# distutils: language = c++
# cython: cdivision = True
# cython: boundscheck = False
# cython: wraparound = False
# cython: profile = False
# cython: language_level = 3

from pymaxion.geometry.Vector3d cimport Vector3d

cdef class Force(Goal):

    def __cinit__(Force self):
        self.goal_n_particles = 1

    def __init__(Force self, list force_vector, list p_index=[]):
        self.move_vectors.push_back(Vector3d(force_vector[0],
                                             force_vector[1],
                                             force_vector[2]))
        self.strength.push_back(1.0)
        
        for ind in p_index:
            self.particle_index.push_back(ind)

