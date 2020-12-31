from pymaxion.goals.goal cimport Goal

cdef class Bar(Goal):
    cdef readonly double E
    cdef readonly double A
    cdef double initial_length
