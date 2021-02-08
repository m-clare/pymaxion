# distutils: language = c++
# cython: cdivision = True
# cython: boundscheck = False
# cython: wraparound = False
# cython: linetrace = True
# cython: language_level = 3

from numpy cimport ndarray
from numpy cimport abs
from pymaxion.geometry.Point3d cimport Point3d

def create_2d_mv(ndarray arr):
    """helper function for creating a 2d memory view on the fly for debugging."""
    cdef double[:, :] mv = arr
    return mv

def create_1d_mv(ndarray arr):
    """helper function for creating a 1d memory view on the fly for debugging."""
    cdef double[:] mv = arr
    return mv

cdef bint pt_within_tolerance(Point3d pt0, Point3d pt1, double tol=1e-3):
    """
    cpp based tolerance check of point distance -- currently not used
    """
    cdef bint x_close, y_close, z_close

    x_close = abs(pt0.x - pt1.x) < tol
    y_close = abs(pt0.y - pt1.y) < tol
    z_close = abs(pt0.z - pt1.z) < tol

    return (x_close & y_close & z_close)

def pos_within_tolerance(tuple pt0, tuple pt1, double tol=1e-3):
    """
    Tolerance check to determine if particle is within 1e-3 of another.

    Returns
    -------
    bool
        True if close.
    """

    x_close = abs(pt0[0] - pt1[0]) < tol
    y_close = abs(pt0[1] - pt1[1]) < tol
    z_close = abs(pt0[2] - pt1[2]) < tol

    return (x_close and y_close and z_close)

