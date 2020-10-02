from pymaxion.geometry.Vector3d cimport Vector3d
from libcpp.vector cimport vector

cdef class Particle:
    cdef Vector3d *position
    cdef Vector3d *start_position
    cdef Vector3d *sum_moves
    cdef Vector3d *velocity
    cdef double sum_weights
    cdef int system_index
    cdef void reset(Particle)
