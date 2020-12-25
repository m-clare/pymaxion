from pymaxion.geometry.Vector3d cimport Vector3d

cdef extern from "Point3d.cpp":
  pass

cdef extern from "Point3d.h" namespace "geometry":
  cdef cppclass Point3d nogil:
    double x, y, z
    Point3d() except +
    Point3d(double x, double y, double z) except +
    Point3d(const Vector3d v) except +
    void move_point(double x, double y, double z)
    void move_point(const Vector3d v)
    void set_point(double x, double y, double z)
    void set_point(const Vector3d v)
