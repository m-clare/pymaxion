from libcpp.vector cimport vector
from pymaxion.goals.goal cimport Goal
from pymaxion.geometry.Point3d cimport Point3d

cdef class Anchor(Goal):
    cdef vector[Point3d] *anchor_pt

    @staticmethod
    cdef Anchor from_Point3d(Point3d pt, double strength)

