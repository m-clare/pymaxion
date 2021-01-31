from libcpp.vector cimport vector
from pymaxion.geometry.Vector3d cimport Vector3d
from pymaxion.geometry.Point3d cimport Point3d

cdef class Constraint:
    cdef public int constraint_n_particles
    cdef vector[int] *particle_index
    cdef vector[Vector3d] *move_vectors
    cdef vector[double] *weighting
    cdef vector[double] *strength
    cdef public list particles
    cdef void calculate(Constraint, double[:,:] arr) nogil
    cdef void sum_moves(Constraint, double[:,:] p_sum, double[:] w_sum) nogil
