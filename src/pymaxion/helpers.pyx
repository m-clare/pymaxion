# distutils: language = c++
# cython: cdivision = True
# cython: boundscheck = False
# cython: wraparound = False
# cython: profile = False
# cython: language_level = 3

from numpy cimport ndarray
from numpy cimport abs
from pymaxion.geometry.Point3d cimport Point3d

def create_2d_mv(ndarray arr):
    cdef double[:, :] mv =  arr
    return mv

def create_1d_mv(ndarray arr):
    cdef double[:] mv = arr
    return mv

cdef bint pt_within_tolerance(Point3d pt0, Point3d pt1, double tol=1e-3):
    cdef bint x_close, y_close, z_close

    x_close = abs(pt0.x - pt1.x) < tol
    y_close = abs(pt0.y - pt1.y) < tol
    z_close = abs(pt0.z - pt1.z) < tol

    return (x_close & y_close & z_close)

def pos_within_tolerance(tuple pt0, tuple pt1, double tol=1e-3):

    x_close = abs(pt0[0] - pt1[0]) < tol
    y_close = abs(pt0[1] - pt1[1]) < tol
    z_close = abs(pt0[2] - pt1[2]) < tol

    return (x_close and y_close and z_close)
    # pt3d1 = Point3d(pt1[0], pt1[1], pt1[2])

    # close = pt_within_tolerance(pt3d0, pt3d1, tol)
    # return close
