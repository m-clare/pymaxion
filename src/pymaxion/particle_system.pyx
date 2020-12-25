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
from numpy cimport ndarray
from libc.stdio cimport printf

from pymaxion.goals.goal cimport Goal
from pymaxion.goals.anchor cimport Anchor
from pymaxion.particle cimport Particle
from pymaxion.geometry.Vector3d cimport Vector3d

cdef class ParticleSystem(object):
    cdef public int n_goals
    cdef public int n_particles
    cdef public int num_iter
    cdef PyObject **goals
    cdef PyObject **particles
    cdef public list ref_goals
    cdef public list ref_particles
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

    def __init__(ParticleSystem self):
        self.ref_goals = []
        self.ref_particles = []

    def __dealloc__(ParticleSystem self):
        if self.goals != NULL:
            free(self.goals)
        if self.particles != NULL:
            free(self.particles)

    cpdef add_particle_to_system(ParticleSystem self, Particle particle):
        particle.system_index = self.n_particles
        self.ref_particles.append(particle)
        self.n_particles += 1

    cpdef add_goal_to_system(ParticleSystem self, Goal goal):
        # Check if goal already has particle indices
        self.ref_goals.append(goal)
        self.n_goals += 1

    cpdef find_particle_index(ParticleSystem self):
        pass

    cpdef assign_particle_index(ParticleSystem self):
        pass

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

    cdef void move_particle(ParticleSystem self, int j, double[:, :] p_moves,
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
            current_particle.position.x = matrix_pos[0]
            current_particle.position.y = matrix_pos[1]
            current_particle.position.z = matrix_pos[2]


    cpdef solve(ParticleSystem self, double ke=1e-15, int max_iter=10000, bint parallel=False):
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
                    self.move_particle(j, p_moves, p_weights, p_pos, p_vel)
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




