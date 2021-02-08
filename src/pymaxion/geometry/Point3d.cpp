#include <iostream>
#include "Vector3d.h"
#include "Point3d.h"

namespace geometry {

  Point3d::Point3d() {}

  Point3d::Point3d(double x, double y, double z = 0.0) {
    this->x = x;
    this->y = y;
    this->z = z;
  }

  Point3d::Point3d(const Vector3d v) {
    this->x = v.x;
    this->y = v.y;
    this->z = v.z;
  }

  Point3d::~Point3d() {}

  void Point3d::move(double x, double y, double z= 0.0) {
    this->x = this->x + x;
    this->y = this->y + y;
    this->z = this->z + z;
  }

  void Point3d::move(const Vector3d v){
    this->x = this->x + v.x;
    this->y = this->y + v.y;
    this->z = this->z + v.z;
  }

  void Point3d::set_position(double x, double y, double z = 0.0) {
    this->x = x;
    this->y = y;
    this->z = z;
  }

  void Point3d::set_position(const Vector3d v) {
    this->x = v.x;
    this->y = v.y;
    this->z = v.z;
  }

  double Point3d::distance_to_point(const Point3d p) {
    double xd, yd, zd;
    xd = this->x - p.x;
    yd = this->y - p.y;
    zd = this->z - p.z;
    return (std::sqrt(xd * xd + yd * yd + zd * zd));
  }
}
