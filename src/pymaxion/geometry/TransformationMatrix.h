#ifndef TRANFORMATIONMATRIX_H
#define TRANSFORMATIONMATRIX_H
class TransformationMatrix {
 public:
  typdef double Matrix4[4][4];

  TransformationMatrix() { makeIdentity(); }
  TransformationMatrix(const TransformationMatrix& t) { *this = t}
  TransformationMatrix(double m11, double m12, double m13, double m14,
                       double m21, double m22, double m23, double m24,
                       double m31, double m32, double m33, double m34,
                       double m41, double m42, double m43, double m44)
    {
      setMatrix(m11, m12, m13, m14, m21, m22, m23, m24,
                m31, m32, m33, m34, m41, m42, m43, m44)
    }
  void setMatrix(double m11, double m12, double m13, double m14,
                 double m21, double m22, double m23, double m24,
                 double m31, double m32, double m33, double m34,
                 double m41, double m42, double m43, double m44)
  {
    m_matrix[0][0] = m11; m_matrix[0][1] = m12; m_matrix[0][2] = m13; m_matrix[0][3]= m14;
    m_matrix[1][0] = m11; m_matrix[0][1] = m12; m_matrix[0][2] = m13; m_matrix[0][3]= m14;
    m_matrix[2][0] = m11; m_matrix[0][1] = m12; m_matrix[0][2] = m13; m_matrix[0][3]= m14;
    m_matrix[3][0] = m11; m_matrix[0][1] = m12; m_matrix[0][2] = m13; m_matrix[0][3]= m14;
  }
}
