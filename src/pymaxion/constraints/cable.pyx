# distutils: language = c++
# cython: cdivision = True
# cython: boundscheck = False
# cython: wraparound = False
# cython: linetrace = True
# cython: language_level = 3


from pymaxion.geometry.Vector3d cimport Vector3d

cdef class Cable(Constraint):

    def __cinit__(Cable self):
        self.constraint_n_particles = 2

    def __init__(Cable self, list particles,
                 double E, double A, double rest_length=0.0,
                 list p_index=[]):
        """
        Cable constraint based on two points.
        Tension only element.
        Cable can be prestressed (initial length different than rest length).
        E corresponds to Elastic (Young's) modulus (N/m^2).
        A corresponds to bar area (m).
        Units conversion to come later.
        """

        if len(particles) != self.constraint_n_particles:
            raise ValueError("Incorrect number of particles for Cable")
        super().__init__(particles)

        self.E = E
        self.A = A

        if rest_length == 0.0:
            # set initial length to current length
            p0 = self.particles[0]
            p1 = self.particles[1]
            self.rest_length = p0.distance_to_particle(p1)
        else:
            self.rest_length = rest_length

        self.move_vectors.push_back(Vector3d(0.0, 0.0, 0.0))
        self.move_vectors.push_back(Vector3d(0.0, 0.0, 0.0))
        self.strength.push_back((2 * E * A) / self.rest_length)
        self.strength.push_back((2 * E * A) / self.rest_length)

    cdef void calculate(Cable self, double[:, :] arr) nogil:
        cdef Vector3d start_pt
        cdef Vector3d end_pt
        cdef double current_length
        cdef double length_diff
        cdef Vector3d force_start
        cdef Vector3d force_end
        cdef Vector3d force_dir

        p1 = self.particle_index[0].at(0)
        p2 = self.particle_index[0].at(1)
        start_pt = Vector3d(arr[p1, 0], arr[p1, 1], arr[p1, 2])
        end_pt = Vector3d(arr[p2, 0], arr[p2, 1], arr[p2, 2])

        force_dir = end_pt.vector_subtract(start_pt)
        current_length = force_dir.length()
        force_dir.vector_unitize()
        length_diff = current_length - self.rest_length
        if length_diff > 0.0:
            force_start = force_dir.vector_scale(0.5 * length_diff)
            force_end = force_dir.vector_scale(-0.5 * length_diff)
        else:
            force_start = Vector3d(0, 0, 0)
            force_end = Vector3d(0, 0, 0)

        self.move_vectors[0].at(0).set_value(force_start)
        self.move_vectors[0].at(1).set_value(force_end)

