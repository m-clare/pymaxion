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

  void Point3d::move_point(double x, double y, double z= 0.0) {
    this->x = this->x + x;
    this->y = this->y + y;
    this->z = this->z + z;
  }

  void Point3d::move_point(const Vector3d v){
    this->x = this->x + v.x;
    this->y = this->y + v.y;
    this->z = this->z + v.z;
  }

  void Point3d::set_point(double x, double y, double z = 0.0) {
    this->x = x;
    this->y = y;
    this->z = z;
  }

  void Point3d::set_point(const Vector3d v) {
    this->x = v.x;
    this->y = v.y;
    this->z = v.z;
  }
}
