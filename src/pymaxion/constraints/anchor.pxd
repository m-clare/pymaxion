from libcpp.vector cimport vector
from pymaxion.constraints.constraint cimport Constraint
from pymaxion.geometry.Point3d cimport Point3d

cdef class Anchor(Constraint):
    cdef vector[Point3d] *anchor_pt

    @staticmethod
    cdef Anchor from_Point3d(Point3d pt, double strength)

