# distutils: language = c++
# cython: cdivision = True
# cython: boundscheck = False
# cython: wraparound = False
# cython: profile = True
# cython: language_level = 3

from pymaxion.geometry.Vector3d cimport Vector3d
from pymaxion.geometry.Point3d cimport Point3d
from libc.stdlib cimport free

cdef class Anchor(Goal):

    def __cinit__(Anchor self):
        self.goal_n_particles = 1
        self.anchor_pt = new vector[Point3d]()

    def __init__(Anchor self, list anchor_pt, double strength=1.0,
                 list particles=[], list p_index=[]):

        self.particles.push_back(Point3d(anchor_pt[0],
                                         anchor_pt[1],
                                         anchor_pt[2]))

        # initialize vectors
        self.anchor_pt.push_back(Point3d(anchor_pt[0],
                                         anchor_pt[1],
                                         anchor_pt[2]))

        self.move_vectors.push_back(Vector3d(0.0, 0.0, 0.0))

        self.strength.push_back(strength)

        if p_index:
            for ind in p_index:
                self.particle_index.push_back(ind)

    def __dealloc__(self):
        if self.anchor_pt != NULL:
            free(self.anchor_pt)

    cdef void calculate(Anchor self, double[:,:] arr) nogil:
        cdef Vector3d cur_pos
        anchor_pt = self.anchor_pt[0].at(0)
        p_index = self.particle_index[0].at(0)
        cur_pos = Vector3d(anchor_pt.x, anchor_pt.y, anchor_pt.z)
        new_pos = cur_pos.vector_subtract(Vector3d(arr[p_index, 0],
                                                     arr[p_index, 1],
                                                     arr[p_index, 2]))
        self.move_vectors[0].at(0).set_value(new_pos.x,
                                             new_pos.y,
                                             new_pos.z)

    @property
    def anchor_pt(Anchor self):
        anchor_pt = self.anchor_pt[0].at(0)
        return anchor_pt.x, anchor_pt.y, anchor_pt.z

    @staticmethod
    cdef Anchor from_Point3d(Point3d pt, double strength):
        cdef Anchor anchor = Anchor.__new__(Anchor)
        anchor.anchor_pt.push_back(pt)
        anchor.move_vectors.push_back(Vector3d(0.0, 0.0, 0.0))
        anchor.strength.push_back(strength)
        return anchor

    @classmethod
    def from_point(cls, list pt, double strength=1.0):
        anchor = cls([pt[0], pt[1], pt[2]], strength)
        return anchor
