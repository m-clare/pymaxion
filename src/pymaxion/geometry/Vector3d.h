#ifndef VECTOR3D_H
#define VECTOR3D_H

namespace geometry {
  class Vector3d {
  public:
    double x, y, z;
    Vector3d();
    Vector3d(double x, double y, double z);
    ~Vector3d();
    double length_squared();
    double length();
    void vector_unitize();
    Vector3d vector_scale(const double s);
    Vector3d vector_add(const Vector3d v);
    Vector3d vector_subtract(const Vector3d v);
    void set_value(const Vector3d v);
    void set_value(double x, double y, double z);
  };
}

#endif
