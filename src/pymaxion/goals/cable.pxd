from pymaxion.goals.goal cimport Goal

cdef class Cable(Goal):
    cdef double E
    cdef double A
    cdef double rest_length
