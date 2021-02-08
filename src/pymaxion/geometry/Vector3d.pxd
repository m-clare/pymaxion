cdef extern from "Vector3d.cpp":
   pass
   
cdef extern from "Vector3d.h" namespace "geometry":
    cdef cppclass Vector3d nogil:
        double x, y, z
        Vector3d() except +
        Vector3d(double x, double y, double z) except +
        double length_squared()
        double length()
        void vector_unitize()
        Vector3d vector_scale(const double s)
        Vector3d vector_add(const Vector3d v)
        Vector3d vector_subtract(const Vector3d v)
        void set_value(const Vector3d v)
        void set_value(double x, double y, double z)
