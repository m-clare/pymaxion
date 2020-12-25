# distutils: language = c++
# cython: cdivision = True
# cython: boundscheck = False
# cython: wraparound = False
# cython: profile = False
# cython: language_level = 3

from pymaxion.geometry.Vector3d cimport Vector3d

cdef class Rod(Goal):

    def __cinit__(Rod self):
        self.goal_n_particles = 4

    def __init__(Rod self, double E, double inertia,
                 double z_distance, double rest_angle, list p_index=[]):
        self.E = E
        self.inertia = inertia
        self.z_distance = z_distance
        self.rest_angle = rest_angle

        for ind in p_index:
            self.particle_index.push_back(ind)

        for i in range(len(p_index)):
            self.move_vectors.push_back(Vector3d(0.0, 0.0, 0.0))
            self.strength.push_back(E*inertia*1e-6)

    cdef void calculate(Rod self, double[:, :] arr) nogil:
        cdef Vector3d pt0
        cdef Vector3d pt1
        cdef Vector3d pt2
        cdef Vector3d pt3

        p0 = self.particle_index[0].at(0)
        p1 = self.particle_index[0].at(1)
        p2 = self.particle_index[0].at(2)
        p3 = self.particle_index[0].at(3)

        pt0 = Vector3d(arr[p0, 0], arr[p0, 1], arr[p0, 2])
        pt1 = Vector3d(arr[p1, 0], arr[p1, 1], arr[p1, 2])
        pt2 = Vector3d(arr[p2, 0], arr[p2, 1], arr[p2, 2])
        pt3 = Vector3d(arr[p3, 0], arr[p3, 1], arr[p3, 2])


