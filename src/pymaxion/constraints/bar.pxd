from pymaxion.constraints.constraint cimport Constraint

cdef class Bar(Constraint):
    cdef readonly double E
    cdef readonly double A
    cdef readonly double initial_length
