from pymaxion.constraints.constraint cimport Constraint

cdef class Rod(Constraint):
    cdef double E
    cdef double inertia
    cdef double z_distance
    cdef double rest_angle
