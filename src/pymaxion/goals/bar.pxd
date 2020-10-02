from pymaxion.goals.goal cimport Goal

cdef class Bar(Goal):
    cdef double E
    cdef double A
    cdef double initial_length
