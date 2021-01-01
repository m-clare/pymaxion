import sys
from time import perf_counter
import cProfile
from pymaxion.goals.anchor import Anchor
from pymaxion.particle_system import ParticleSystem
from pymaxion.particle import Particle
from pymaxion.goals.cable import Cable
from pymaxion.goals.force import Force
import numpy as np


def create_sample_system(parallel=False):

    psystem = ParticleSystem()

    pt1 = Particle(0, 0, 0)
    pt2 = Particle(1, 0, 0)
    pt3 = Particle(2, 0, 0)

    E = 210000
    A = 20 ** 2.0 * np.pi / 4.0
    load = -1e6

    cp1 = Anchor([Particle(0, 0, 0)], 1e20)
    cp2 = Anchor([Particle(2, 0, 0)], 1e20)
    cp3 = Cable([pt1, pt2], E, A, 1.0)
    cp4 = Cable([pt2, pt3], E, A, 1.0)
    cp5 = Force([pt2], [0, 0, load])

    particles = [pt1, pt2, pt3]
    constraints = [cp1, cp2, cp3, cp4, cp5]

    for particle in particles:
        psystem.add_particle_to_system(particle)
    for goal in constraints:
        psystem.add_goal_to_system(goal)

    psystem.solve(max_iter=1000, parallel=parallel)
    print(psystem.particle_velocities)
    print(psystem.particle_positions)
    print(psystem.num_iter)

cProfile.run('create_sample_system(False)')

