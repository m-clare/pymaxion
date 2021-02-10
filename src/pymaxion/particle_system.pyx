# distutils: language = c++
# cython: cdivision = True
# cython: boundscheck = False
# cython: wraparound = False
# cython: linetrace = True
# cython: language_level = 3

cimport cython
from cpython cimport PyObject
from cython.parallel import parallel, prange
from libc.stdlib cimport malloc, free
from libcpp.vector cimport vector
from numpy cimport ndarray
from numpy import zeros
from numpy import double as npd
import json

# Fix to have single import for all constraints
from pymaxion.constraints.constraint cimport Constraint
from pymaxion.constraints.anchor cimport Anchor
from pymaxion.constraints.cable cimport Cable
from pymaxion.constraints.force cimport Force
from pymaxion.particle cimport Particle
from pymaxion.geometry.Vector3d cimport Vector3d
from pymaxion.geometry.Point3d cimport Point3d
from pymaxion.helpers import pos_within_tolerance

cdef class ParticleSystem(object):
    """System basis for simulation composed of particles and the relationships between them based on constraints.

    Attributes
    ----------
    ref_particles: list
       Particles in the system as defined by their (x, y, z) coordinates.
       They cannot occupy the same (x, y, z) coordinates at the start of simulation else they will be merged.

    ref_constraints: list
        List of relationships between particles based on their current x,y,z position and constraint weighting.
    """
    cdef public int n_constraints
    cdef public int n_particles
    cdef public int num_iter
    cdef public double tol
    cdef PyObject **constraints
    cdef PyObject **particles
    cdef public list ref_constraints
    cdef public list ref_particles
    cdef public dict ref_positions
    cdef public ndarray particle_positions
    cdef public ndarray particle_sum_moves
    cdef public ndarray particle_sum_weights
    cdef public ndarray particle_velocities

    def __cinit__(ParticleSystem self):
        self.constraints = NULL
        self.particles = NULL
        self.n_constraints = 0
        self.n_particles = 0
        self.num_iter = 0

    def __init__(ParticleSystem self):
        self.ref_constraints = []
        self.ref_particles = []
        self.ref_positions = {}

    def __dealloc__(ParticleSystem self):
        if self.constraints != NULL:
            free(self.constraints)
        if self.particles != NULL:
            free(self.particles)

    @classmethod
    def from_json(cls, filepath):
        """
        Construct particle system from json file.
        """
        with open(filepath, 'r') as fh:
            data = json.load(fh)
        points = data['Particles']
        cables = data['Cables']
        anchors = data['Anchors']
        forces = data['Forces']

        ps = cls()
        for pt in points:
            ps.add_particle_to_system(Particle(pt[0], pt[1], pt[2]))

        for key, attr in cables.items():
            p_ind = eval(key)
            p0 = ps.ref_particles[p_ind[0]]
            p1 = ps.ref_particles[p_ind[1]]
            E = attr['E']
            A = attr['A']
            cable = Cable([p0, p1], E, A)
            ps.add_constraint_to_system(cable)

        for key, attr in anchors.items():
            p_ind = eval(key)
            strength = attr['strength']
            p0 = ps.ref_particles[p_ind]
            anchor = Anchor([p0], strength)
            ps.add_constraint_to_system(anchor)

        for key, attr in forces.items():
            p_ind = eval(key)
            p0 = ps.ref_particles[p_ind]
            force = Force([p0], attr)
            ps.add_constraint_to_system(force)

        return ps

    @classmethod
    def to_json(ParticleSystem self, filepath):
        pass

    cpdef add_particle_to_system(ParticleSystem self, Particle particle):
        p_ind = self.find_particle_index(particle)
        if p_ind is None:
            pos = particle.position[0]
            self.ref_particles.append(particle)
            p_ind = self.assign_particle_index(particle)
            self.ref_positions.update({(round(pos.x, 3),
                                        round(pos.y, 3),
                                        round(pos.z, 3)): p_ind})
        return p_ind

    cpdef add_particles_to_system(ParticleSystem self, list particles):
        """
        Add particles to a particle system based on a list of particles.
        """
        for particle in particles:
            self.add_particle_to_system(particle)

    cpdef add_constraint_to_system(ParticleSystem self, Constraint constraint):
        """
        Add constraint to a particle system.
        """
        for particle in constraint.particles:
            p_ind = self.find_particle_index(particle)
            if p_ind is None:
                self.ref_particles.append(particle)
                pos = particle.position
                p_ind = self.assign_particle_index(particle)
                self.ref_position.update({(round(pos.x, 3),
                                           round(pos.y, 3),
                                           round(pos.z, 3)): p_ind})
            constraint.particle_index.push_back(p_ind)
        self.ref_constraints.append(constraint)
        self.n_constraints += 1

    cpdef add_constraints_to_system(ParticleSystem self, list constraints):
        """
        Add constraints to a particle system based on a list of constraints.
        """
        for constraint in constraints:
            self.add_constraint_to_system(constraint)

    cpdef find_particle_index(ParticleSystem self, Particle particle):
        """
        Retrieve particle index (int) if it is a particle already in the particle system.
        Current tolerance is 1e-3 for merging particle positions.
        """
        pos = particle.position[0]
        trunc = (round(pos.x, 3), round(pos.y, 3), round(pos.z, 3))
        if trunc in self.ref_positions:
            return self.ref_positions[trunc]

    cpdef assign_particle_index(ParticleSystem self, Particle particle):
        """
        Assign a particle index to a particle.
        """
        particle.system_index = self.n_particles # zero indexed
        self.n_particles += 1
        return particle.system_index

    cpdef initialize_system(ParticleSystem self):
        """ 
        Initialize numpy matrices for vector solve (memory views in Cython).
        """
        cdef int i
        self.particle_positions   = zeros((self.n_particles, 3),
                                           dtype=npd)
        self.particle_velocities  = zeros((self.n_particles, 3),
                                           dtype=npd)
        self.particle_sum_moves   = zeros((self.n_particles, 3),
                                           dtype=npd)
        self.particle_sum_weights = zeros((self.n_particles),
                                           dtype=npd)
        for i in range(self.n_particles):
            particle = self.ref_particles[i]
            self.particle_positions[i, :] = particle.position
            self.particle_velocities[i,:] = particle.velocity

    cpdef finalize_system(ParticleSystem self):
        """
        Update particle objects with their new positions at end of solve.
        """
        for i in range(self.n_particles):
            matrix_pos = self.particle_positions[i]
            current_particle = self.ref_particles[i]
            cx, cy, cz = matrix_pos[0], matrix_pos[1], matrix_pos[2]
            current_particle.set_position(cx, cy, cz)

    cpdef solve(ParticleSystem self, double ke=1e-10, int max_iter=10000,
                bint parallel=False):
        """
        Main solve method for projective DR.
        """
        cdef int i
        cdef int j
        cdef bint flag
        cdef double v_sum
        cdef double tx, ty, tz
        cdef double px, py, pz
        cdef double vx, vy, vz

        self.initialize_system()
        flag = False
        self.num_iter = 0
        # memory view must be created before nogil
        cdef double [:, :] p_pos = self.particle_positions
        cdef double [:, :] p_vel = self.particle_velocities
        cdef double [:, :] p_moves = self.particle_sum_moves
        cdef double [:]  p_weights = self.particle_sum_weights
        # set up C++ only objects for nogil
        self.constraints = <PyObject **>malloc(self.n_constraints*cython.sizeof(
                                         cython.pointer(PyObject)))
        for i in range(self.n_constraints):
            self.constraints[i] = <PyObject*>self.ref_constraints[i]
        with nogil:
            while flag == False:
                for j in range(self.n_particles):
                    p_pos[j, 0] = p_pos[j, 0] + p_vel[j, 0]
                    p_pos[j, 1] = p_pos[j, 1] + p_vel[j, 1]
                    p_pos[j, 2] = p_pos[j, 2] + p_vel[j, 2]
                for j in range(self.n_constraints):
                    (<Constraint?>self.constraints[j]).calculate(p_pos)
                for j in range(self.n_constraints):
                    (<Constraint?>self.constraints[j]).sum_moves(p_moves, p_weights)
                for j in range(self.n_particles):
                    if (p_moves[j, 0] == 0.0 and
                        p_moves[j, 1] == 0.0 and
                        p_moves[j, 2] == 0.0):
                        p_vel[j] = 0.0
                    else:
                        tx = p_moves[j, 0] / p_weights[j]
                        ty = p_moves[j, 1] / p_weights[j]
                        tz = p_moves[j, 2] / p_weights[j]
                        px = p_pos[j, 0] + tx
                        py = p_pos[j, 1] + ty
                        pz = p_pos[j, 2] + tz
                        vx = p_vel[j, 0] + tx
                        vy = p_vel[j, 1] + ty
                        vz = p_vel[j, 2] + tz
                        if ((tx * vx + ty * vy + tz * vz) < 0.0):
                            p_vel[j, 0] = vx * 0.9
                            p_vel[j, 1] = vy * 0.9
                            p_vel[j, 2] = vz * 0.9
                        else:
                            p_vel[j, 0] = vx
                            p_vel[j, 1] = vy
                            p_vel[j, 2] = vz
                    p_moves[j] = 0.0
                    p_weights[j] = 0.0
                self.num_iter += 1
                v_sum = 0.0
                for j in range(self.n_particles):
                    v_sum += p_vel[j, 0] * p_vel[j, 0] + \
                             p_vel[j, 1] * p_vel[j, 1] + \
                             p_vel[j, 2] * p_vel[j, 2]
                v_sum = v_sum / self.n_particles
                if v_sum < ke or max_iter <= self.num_iter:
                    flag = True
