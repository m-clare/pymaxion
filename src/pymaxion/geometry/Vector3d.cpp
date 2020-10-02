#include <iostream>
#include "Vector3d.h"

namespace geometry {

  Vector3d::Vector3d() {}

  Vector3d::Vector3d(double x, double y, double z = 0.0) {
    this->x = x;
    this->y = y;
    this->z = z;
  }

  Vector3d::~Vector3d () {}

  double Vector3d::length_squared(){
    return (this->x * this->x + this->y * this->y + this->z * this->z);
  }

  double Vector3d::length(){
    double ls = this->x*this->x + this->y*this->y + this->z*this->z;
    return (std::sqrt(ls));
  }

  void Vector3d::vector_unitize() {
    double length = Vector3d::length();
    this->x = this->x / length;
    this->y = this->y / length;
    this->z = this->z / length;
  }

  Vector3d Vector3d::vector_scale(const double s) {
    Vector3d vector;
    vector.x = this->x * s;
    vector.y = this->y * s;
    vector.z = this->z * s;
    return vector;
  }

  Vector3d Vector3d::vector_add(const Vector3d v) {
    Vector3d vector;
    vector.x = this->x + v.x;
    vector.y = this->y + v.y;
    vector.z = this->z + v.z;
    return vector;
    }

  Vector3d Vector3d::vector_subtract(const Vector3d v) {
    Vector3d vector;
    vector.x = this->x - v.x;
    vector.y = this->y - v.y;
    vector.z = this->z - v.z;
    return vector;
  }

  void Vector3d::set_value(const Vector3d v) {
    this->x = v.x;
    this->y = v.y;
    this->z = v.z;
  }

  void Vector3d::set_value(double x, double y, double z) {
    this->x = x;
    this->y = y;
    this->z = z;
  }
}

