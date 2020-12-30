from libcpp.vector cimport vector
from pymaxion.geometry.Vector3d cimport Vector3d
from pymaxion.geometry.Point3d cimport Point3d

cdef class Goal:
    cdef public int goal_n_particles
    cdef vector[int] *particle_index
    cdef vector[Vector3d] *move_vectors
    cdef vector[double] *weighting
    cdef vector[double] *strength
    # cdef public list particles
    cdef void calculate(Goal, double[:,:] arr) nogil
    cdef void sum_moves(Goal, double[:,:] p_sum, double[:] w_sum) nogil
