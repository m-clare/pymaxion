from pymaxion.constraints.constraint cimport Constraint

cdef class Cable(Constraint):
    cdef readonly double E
    cdef readonly double A
    cdef readonly double rest_length
