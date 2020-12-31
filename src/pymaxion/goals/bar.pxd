from pymaxion.goals.goal cimport Goal

cdef class Bar(Goal):
    cdef readonly double E
    cdef readonly double A
    cdef readonly double initial_length
