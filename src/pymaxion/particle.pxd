from pymaxion.geometry.Vector3d cimport Vector3d
from pymaxion.geometry.Point3d cimport Point3d
from libcpp.vector cimport vector

cdef class Particle:
    cdef Point3d *position
    cdef Point3d *start_position
    cdef Vector3d *sum_moves
    cdef Vector3d *velocity
    cdef double sum_weights
    cdef int system_index
    cdef void reset(Particle)
    cpdef distance_to_particle(Particle, Particle particle)
