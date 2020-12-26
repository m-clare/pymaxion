#ifndef POINT3D_H
#define POINT3D_H
#include "Vector3d.h"

namespace geometry {
  class Point3d {
  public:
    double x, y, z;
    Point3d();
    Point3d(double x, double y, double z);
    Point3d(const Vector3d v);
    ~Point3d();
    void move(double x, double y, double z);
    void move(const Vector3d v);
    void set_position(double x, double y, double z);
    void set_position(const Vector3d v);
  };
}

#endif
