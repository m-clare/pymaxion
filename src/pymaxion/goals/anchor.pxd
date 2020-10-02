from libcpp.vector cimport vector
from pymaxion.goals.goal cimport Goal
from pymaxion.geometry.Vector3d cimport Vector3d

cdef class Anchor(Goal):
    cdef vector[Vector3d] *anchor_pt

