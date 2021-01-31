# distutils: language = c++
# cython: cdivision = True
# cython: boundscheck = False
# cython: wraparound = False
# cython: profile = True
# cython: language_level = 3

from libc.stdlib cimport free
from pymaxion.geometry.Vector3d cimport Vector3d
from pymaxion.particle cimport Particle
import numpy as np

cdef class Constraint(object):

    def __cinit__(Constraint self):
        self.particle_index = new vector[int]()
        self.move_vectors = new vector[Vector3d]()
        self.weighting = new vector[double]()
        self.strength = new vector[double]()
        self.constraint_n_particles = 1 # min particle number

    def __init__(Constraint self, list particles=[]):
        self.particles = []

        for particle in particles:
            if not isinstance(particle, Particle):
                raise TypeError("Constraint must be created with a reference particle!")
            else:
                self.particles.append(particle)

    def __dealloc__(self):
        if self.particle_index != NULL:
            free(self.particle_index)
        if self.move_vectors != NULL:
            free(self.move_vectors)
        if self.weighting != NULL:
            free(self.weighting)
        if self.strength != NULL:
            free(self.strength)

    cdef void calculate(Constraint self, double[:,:] arr) nogil:
        pass

    cdef void sum_moves(Constraint self, double[:,:] p_sum, double[:] w_sum) nogil:
        cdef int i
        for i in range(self.constraint_n_particles):
            p_index = self.particle_index[0].at(i)
            curr_move = self.move_vectors[0].at(i)
            curr_strength = self.strength[0].at(i)
            w_sum[p_index] += curr_strength
            p_sum[p_index, 0] += curr_move.x * curr_strength
            p_sum[p_index, 1] += curr_move.y * curr_strength
            p_sum[p_index, 2] += curr_move.z * curr_strength

    @property
    def particle_index(Constraint self):
        return [ind for ind in self.particle_index[:1]][0]

    @property
    def move_vectors(Constraint self):
        mvs = np.zeros((self.constraint_n_particles, 3), dtype=np.double)
        for i in range(self.constraint_n_particles ):
            mv = self.move_vectors[0].at(i)
            mvs[i, 0] = mv.x
            mvs[i, 1] = mv.y
            mvs[i, 2] = mv.z
        return mvs

    @property
    def weighting(Constraint self):
        return [weighting for weighting in self.weighting[:1]][0]

    @property
    def strength(Constraint self):
        return [strength for strength in self.strength[:1]][0]

    def py_calculate(Constraint self, double[:, :] arr):
        return self.calculate(arr)

    def py_sum_moves(Constraint self, double[:,:] p_sum, double[:] w_sum):
        return self.sum_moves(p_sum, w_sum)


