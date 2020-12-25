from libcpp.vector cimport vector
from pymaxion.goals.goal cimport Goal
from pymaxion.geometry.Point3d cimport Point3d

cdef class Anchor(Goal):
    cdef vector[Point3d] *anchor_pt

