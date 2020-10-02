# distutils: language = c++
# cython: cdivision = True
# cython: boundscheck = False
# cython: wraparound = False
# cython: profile = True
# cython: language_level = 3

from pymaxion.geometry.Vector3d cimport Vector3d
from libc.stdlib cimport free

cdef class Anchor(Goal):

    def __cinit__(Anchor self):
        self.goal_n_particles = 1
        self.anchor_pt = new vector[Vector3d]()

    def __init__(Anchor self,
                 list anchor_pt,
                 double strength,
                 list p_index):

        # initialize vectors
        self.anchor_pt.push_back(Vector3d(anchor_pt[0],
                                          anchor_pt[1],
                                          anchor_pt[2]))

        self.move_vectors.push_back(Vector3d(0.0, 0.0, 0.0))

        self.strength.push_back(strength)

        for ind in p_index:
            self.particle_index.push_back(ind)

    def __dealloc__(self):
        if self.anchor_pt != NULL:
            free(self.anchor_pt)

    cdef void calculate(Anchor self, double[:,:] arr) nogil:
        anchor_pt = self.anchor_pt[0].at(0)
        p_index = self.particle_index[0].at(0)
        new_pos = anchor_pt.vector_subtract(Vector3d(arr[p_index, 0],
                                                     arr[p_index, 1],
                                                     arr[p_index, 2]))
        self.move_vectors[0].at(0).set_value(new_pos.x,
                                             new_pos.y,
                                             new_pos.z)

    @property
    def anchor_pt(Anchor self):
        anchor_pt = self.anchor_pt[0].at(0)
        return anchor_pt.x, anchor_pt.y, anchor_pt.z

