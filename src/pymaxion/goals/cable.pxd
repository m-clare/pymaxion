from pymaxion.goals.goal cimport Goal

cdef class Cable(Goal):
    cdef readonly double E
    cdef readonly double A
    cdef readonly double rest_length
