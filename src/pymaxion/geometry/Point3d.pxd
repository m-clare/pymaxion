from pymaxion.geometry.Vector3d cimport Vector3d

cdef extern from "Point3d.cpp":
  pass

cdef extern from "Point3d.h" namespace "geometry":
  cdef cppclass Point3d nogil:
    double x, y, z
    Point3d() except +
    Point3d(double x, double y, double z) except +
    Point3d(const Vector3d v) except +
    void move(double x, double y, double z)
    void move(const Vector3d v)
    void set_position(double x, double y, double z)
    void set_position(const Vector3d v)
    double distance_to_point(const Point3d p)
