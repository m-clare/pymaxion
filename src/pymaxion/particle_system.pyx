# distutils: language = c++
# cython: cdivision = True
# cython: boundscheck = False
# cython: wraparound = False
# cython: profile = True
# cython: language_level = 3

cimport cython
import numpy as np
from cpython cimport PyObject
from cython.parallel import parallel, prange
from libc.stdlib cimport malloc, free
from libcpp.vector cimport vector
from numpy cimport ndarray
from libc.stdio cimport printf

from pymaxion.goals.goal cimport Goal
from pymaxion.goals.anchor cimport Anchor
from pymaxion.particle cimport Particle
from pymaxion.geometry.Vector3d cimport Vector3d
from pymaxion.geometry.Point3d cimport Point3d
from pymaxion.helpers cimport pt_within_tolerance
from pymaxion.helpers import pos_within_tolerance

cdef class ParticleSystem(object):
    cdef public int n_goals
    cdef public int n_particles
    cdef public int num_iter
    cdef public double tol
    cdef PyObject **goals
    cdef PyObject **particles
    cdef vector[Point3d] *initial_positions
    cdef public list ref_goals
    cdef public list ref_particles
    cdef public list ref_positions
    cdef public ndarray particle_positions
    cdef public ndarray particle_sum_moves
    cdef public ndarray particle_sum_weights
    cdef public ndarray particle_velocities

    def __cinit__(ParticleSystem self):
        self.goals = NULL
        self.particles = NULL
        self.n_goals = 0
        self.n_particles = 0
        self.num_iter = 0

    def __init__(ParticleSystem self, tol=1e-2):
        self.ref_goals = []
        self.ref_particles = []
        self.ref_positions = []
        self.tol = tol

    def __dealloc__(ParticleSystem self):
        if self.goals != NULL:
            free(self.goals)
        if self.particles != NULL:
            free(self.particles)

    def from_json(ParticleSystem self):
        pass

    def to_json(ParticleSystem self):
        pass

    cpdef add_particle_to_system(ParticleSystem self, Particle particle):
        # Check if particle position already exists in system
        p_ind = self.find_particle_index(particle)
        if p_ind is None:
            pos = particle.position[0]
            self.ref_particles.append(particle)
            self.ref_positions.append((pos.x, pos.y, pos.z))
            p_ind = self.assign_particle_index(particle)
        return p_ind

    cpdef add_particles_to_system(ParticleSystem self, list particles):
        for particle in particles:
            self.add_particle_to_system(particle)

    cpdef add_goal_to_system(ParticleSystem self, Goal goal, only_existing=False):
        for particle in goal.particles:
            p_ind = self.find_particle_index(particle)
            if only_existing:
                if p_ind is None:
                    raise ValueError("Goal particle is not part of Particle System")
            else:
                if p_ind is None:
                    self.ref_particles.append(particle)
                    pos = particle.position
                    self.ref_positions.append((pos[0], pos[1], pos[2]))
                    p_ind = self.assign_particle_index(particle)
                goal.particle_index.push_back(p_ind)
        self.ref_goals.append(goal)
        self.n_goals += 1

    cpdef add_goals_to_system(ParticleSystem self, list goals):
        for goal in goals:
            self.add_goal_to_system(goal, False)

    cpdef find_particle_index(ParticleSystem self, Particle particle):
        pos = particle.position[0]
        for i, e in enumerate(self.ref_positions):
            if pos_within_tolerance(e, (pos.x, pos.y, pos.z), self.tol):
                return i

    cpdef assign_particle_index(ParticleSystem self, Particle particle):
        particle.system_index = self.n_particles # zero indexed

        self.n_particles = self.n_particles + 1
        return particle.system_index

    cpdef initialize_system(ParticleSystem self):
        '''
        Initialize matrices for vector solve
        '''
        cdef int i
        self.particle_positions   = np.zeros((self.n_particles, 3),
                                            dtype=np.double)
        self.particle_velocities  = np.zeros((self.n_particles, 3),
                                            dtype=np.double)
        self.particle_sum_moves   = np.zeros((self.n_particles, 3),
                                            dtype=np.double)
        self.particle_sum_weights = np.zeros((self.n_particles),
                                             dtype=np.double)
        for i in range(self.n_particles):
            particle = self.ref_particles[i]
            self.particle_positions[i, :] = particle.position
            self.particle_velocities[i,:] = particle.velocity

    cdef void move_particles(ParticleSystem self, int j, double[:, :] p_moves,
                            double[:] p_weights, double[:, :] p_pos,
                            double[:, :] p_vel) nogil:
        '''
        Global move for particles once local solve completed
        '''
        cdef double nx, ny, nz
        cdef double vx, vy, vz
        cdef Vector3d p_sum
        nx = 0.0
        ny = 0.0
        nz = 0.0
        if p_weights[j] != 0.0:
            nx = p_moves[j, 0] / p_weights[j]
            ny = p_moves[j, 1] / p_weights[j]
            nz = p_moves[j, 2] / p_weights[j]
        vx = p_vel[j, 0] + nx
        vy = p_vel[j, 1] + ny
        vz = p_vel[j, 2] + nz
        if (nx*vx + ny*vy + nz*vz) < 0.0:
            # reversed direction slowdown
            vx = vx * 0.9
            vy = vy * 0.9
            vz = vz * 0.9
        p_pos[j, 0] += nx
        p_pos[j, 1] += ny
        p_pos[j, 2] += nz
        p_sum = Vector3d(nx, ny, nz)
        if (p_sum.length() < 1e-6):
            vx = 0.0
            vy = 0.0
            vz = 0.0
        p_vel[j, 0] = vx
        p_vel[j, 1] = vy
        p_vel[j, 2] = vz

    cpdef finalize_system(ParticleSystem self):
        '''
        Update particle objects with their new positions
        '''
        for i in range(self.n_particles):
            matrix_pos = self.particle_positions[i]
            current_particle = self.ref_particles[i]
            cx, cy, cz = matrix_pos[0], matrix_pos[1], matrix_pos[2]
            current_particle.set_position(cx, cy, cz)

    cpdef solve(ParticleSystem self, double ke=1e-15, int max_iter=10000,
                bint parallel=False):
        cdef int i
        cdef int j
        cdef bint flag
        cdef double v_sum

        # assemble position matrix
        self.initialize_system()
        flag = False
        self.num_iter = 0
        # memory view must be created before nogil
        cdef double [:, :] p_pos = self.particle_positions
        cdef double [:, :] p_vel = self.particle_velocities
        cdef double [:, :] p_moves = self.particle_sum_moves
        cdef double [:]  p_weights = self.particle_sum_weights
        # set up C++ only objects for nogil
        self.goals = <PyObject **>malloc(self.n_goals*cython.sizeof(
                                         cython.pointer(PyObject)))
        for i in range(self.n_goals):
            self.goals[i] = <PyObject*>self.ref_goals[i]
        for i in range(max_iter):
            if flag == True:
                break
            # release GIL for parallel constraint solve
            with nogil:
                '''
                System local goal solve
                '''
                if parallel:
                    for j in prange(self.n_goals):
                        (<Goal?>self.goals[j]).calculate(p_pos)
                    for j in range(self.n_goals):
                        (<Goal?>self.goals[j]).sum_moves(p_moves, p_weights)
                else:
                    for j in range(self.n_goals):
                        (<Goal?>self.goals[j]).calculate(p_pos)
                    for j in range(self.n_goals):
                        (<Goal?>self.goals[j]).sum_moves(p_moves, p_weights)
                # move the particles
                for j in range(self.n_particles):
                    self.move_particles(j, p_moves, p_weights, p_pos, p_vel)
                v_sum = 0.0
                for j in range(self.n_particles):
                    v_sum += p_vel[j, 0] * p_vel[j, 0] + \
                             p_vel[j, 1] * p_vel[j, 1] + \
                             p_vel[j, 2] * p_vel[j, 2]
                v_sum = v_sum / self.n_particles
                if v_sum < ke:
                    flag = True
                # reset moves and weights
                self.num_iter+= 1
                p_weights[:] = 0.0
                p_moves[:, :] = 0.0

    # TO BE REMOVED ?? FLAG INSTEAD?
    cpdef solve_animate(ParticleSystem self, double ke=1e-10, int max_iter=10000, bint parallel=False, int step=10):
        cdef int i
        cdef int j
        cdef int k
        cdef bint flag
        cdef double v_sum
        cdef double[:, :, :] frames = np.zeros((self.n_particles, 3,
                                                max_iter // step + 1),
                                                dtype=np.double)

        # assemble position matrix
        self.initialize_system()
        flag = False
        self.num_iter = 0
        k = 0
        # memory view must be created before nogil
        cdef double [:, :] p_pos = self.particle_positions
        cdef double [:, :] p_vel = self.particle_velocities
        cdef double [:, :] p_moves = self.particle_sum_moves
        cdef double [:]  p_weights = self.particle_sum_weights
        # set up C++ only objects for nogil
        self.goals = <PyObject **>malloc(self.n_goals*cython.sizeof(
                                         cython.pointer(PyObject)))
        for i in range(self.n_goals):
            self.goals[i] = <PyObject*>self.ref_goals[i]
        for i in range(max_iter):
            if flag == True:
                frames[:, :, k] = p_pos
                break
            # release GIL for parallel constraint solve
            with nogil:
                if parallel:
                    for j in prange(self.n_goals):
                        (<Goal?>self.goals[j]).calculate(p_pos)
                    for j in prange(self.n_goals):
                        (<Goal?>self.goals[j]).sum_moves(p_moves, p_weights)
                else:
                    for j in range(self.n_goals):
                        (<Goal?>self.goals[j]).calculate(p_pos)
                    for j in range(self.n_goals):
                        (<Goal?>self.goals[j]).sum_moves(p_moves, p_weights)
                # move the particles
                for j in range(self.n_particles):
                    self.move_particles(j, p_moves, p_weights, p_pos, p_vel)
                v_sum = 0.0
                for j in range(self.n_particles):
                    v_sum += p_vel[j, 0] * p_vel[j, 0] + \
                                  p_vel[j, 1] * p_vel[j, 1] + \
                                  p_vel[j, 2] * p_vel[j, 2]
                v_sum = v_sum / self.n_particles
                if v_sum < ke:
                    flag = True
                    # reset moves and weights
                self.num_iter+= 1
                p_weights[:] = 0.0
                p_moves[:, :] = 0.0
                if (i % 10 == 0):
                    frames[:, :, k] = p_pos
                    k += 1

        return frames







