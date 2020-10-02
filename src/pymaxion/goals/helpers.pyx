# distutils: language = c++
# cython: cdivision = True
# cython: boundscheck = False
# cython: wraparound = False
# cython: profile = False
# cython: language_level = 3

from numpy cimport ndarray

def create_2d_mv(ndarray arr):
    cdef double[:, :] mv =  arr
    return mv

def create_1d_mv(ndarray arr):
    cdef double[:] mv = arr
    return mv
