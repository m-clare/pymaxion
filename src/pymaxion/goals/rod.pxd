from pymaxion.goals.goal cimport Goal

cdef class Rod(Goal):
    cdef double E
    cdef double inertia
    cdef double z_distance
    cdef double rest_angle
