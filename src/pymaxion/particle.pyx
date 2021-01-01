# distutils: language = c++
# cython: cdivision = True
# cython: boundscheck = False
# cython: wraparound = False
# cython: profile = False
# cython: language_level = 3

from pymaxion.geometry.Vector3d cimport Vector3d
from pymaxion.geometry.Point3d cimport Point3d
from libc.stdlib cimport free

cdef class Particle(object):

    def __cinit__(Particle self):
        self.position = new Point3d()
        self.start_position = new Point3d()
        self.sum_moves = new Vector3d()
        self.velocity = new Vector3d()
        self.sum_weights = 0.0
        self.system_index = 0 # index is 0 until particle is added to a system

    def __init__(Particle self, double x, double y, double z):
        self.position.set_position(x, y, z)
        self.start_position.set_position(x, y, z)
        self.sum_moves.set_value(0, 0, 0)
        self.velocity.set_value(0, 0, 0)

    def __dealloc__(self):
        if self.position != NULL:
            free(self.position)
        if self.start_position != NULL:
            free(self.start_position)
        if self.sum_moves != NULL:
            free(self.sum_moves)
        if self.velocity != NULL:
            free(self.velocity)

    cdef void reset(Particle self):
        self.sum_moves.set_value(0.0, 0.0, 0.0)
        self.velocity.set_value(0.0, 0.0, 0.0)
        self.sum_weights = 0.0

    @property
    def position(Particle self):
        return self.position.x, self.position.y, self.position.z

    @property
    def start_position(Particle self):
        return self.start_position.x, self.start_position.y, self.start_position.z

    @property
    def sum_moves(Particle self):
        return self.sum_moves.x, self.sum_moves.y, self.sum_moves.z

    @property
    def velocity(Particle self):
        return self.velocity.x, self.velocity.y, self.velocity.z

    @property
    def sum_weights(Particle self):
        return self.sum_weights

    @property
    def system_index(Particle self):
        return self.system_index

    cpdef distance_to_particle(Particle self, Particle particle):
        p0 = self.position[0]
        p1 = particle.position[0]
        return p0.distance_to_point(p1)
