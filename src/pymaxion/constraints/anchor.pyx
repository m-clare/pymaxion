# distutils: language = c++
# cython: cdivision = True
# cython: boundscheck = False
# cython: wraparound = False
# cython: line_trace = True
# cython: language_level = 3


from pymaxion.geometry.Vector3d cimport Vector3d
from pymaxion.geometry.Point3d cimport Point3d
from pymaxion.particle cimport Particle
from libc.stdlib cimport free

cdef class Anchor(Constraint):

    def __cinit__(Anchor self):
        self.constraint_n_particles = 1
        self.anchor_pt = new vector[Point3d]()

    def __init__(Anchor self, list particles, double strength=1.0,
                 list anchor_pt=[], list p_index=[]):
        """
        Anchor constraint based on a single particle in a list with a given strength.
        Anchor point can be set to different location than that of the current particle position.
        """

        if len(particles) != self.constraint_n_particles:
            raise ValueError("Incorrect number of particles for Anchor")
        super().__init__(particles)

        # initialize vectors
        if not anchor_pt:
            x, y, z = self.particles[0].position
            self.anchor_pt.push_back(Point3d(x, y, z))
        else:
            self.anchor_pt.push_back(Point3d(anchor_pt[0],
                                             anchor_pt[1],
                                             anchor_pt[2]))

        self.move_vectors.push_back(Vector3d(0.0, 0.0, 0.0))

        self.strength.push_back(strength)

        # Add particle by p_index only if it exists... housekeeping
        if p_index:
            for ind in p_index:
                self.particle_index.push_back(ind)

    def __dealloc__(self):
        if self.anchor_pt != NULL:
            free(self.anchor_pt)

    cdef void calculate(Anchor self, double[:,:] arr) nogil:
        cdef Vector3d destination_pos
        anchor_pt = self.anchor_pt[0].at(0)
        p_index = self.particle_index[0].at(0)
        destination_pos = Vector3d(anchor_pt.x, anchor_pt.y, anchor_pt.z)
        difference = destination_pos.vector_subtract(Vector3d(arr[p_index, 0],
                                                              arr[p_index, 1],
                                                              arr[p_index, 2]))
        self.move_vectors[0].at(0).set_value(difference.x,
                                             difference.y,
                                             difference.z)

    @property
    def anchor_pt(Anchor self):
        anchor_pt = self.anchor_pt[0].at(0)
        return anchor_pt.x, anchor_pt.y, anchor_pt.z

    @staticmethod
    cdef Anchor from_Point3d(Point3d pt, double strength):
        cdef Anchor anchor = Anchor.__new__(Anchor)
        anchor.anchor_pt.push_back(pt)
        anchor.move_vectors.push_back(Vector3d(0.0, 0.0, 0.0))
        anchor.strength.push_back(strength)
        return anchor

    @classmethod
    def from_pt(cls, list pt, double strength=1.0):
        particle = Particle(pt[0], pt[1], pt[2])
        anchor = cls([particle], strength)
        return anchor

