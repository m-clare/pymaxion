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

    cp1 = Anchor([0, 0, 0], 1e20, [0])
    cp2 = Anchor([2, 0, 0], 1e20, [2])
    cp3 = Cable(E, A, 1.0, [0, 1])
    cp4 = Cable(E, A, 1.0, [1, 2])
    cp5 = Force([0, 0, load], [1])

    particles = [pt1, pt2, pt3]
    constraints = [cp1, cp2, cp3, cp4, cp5]

    for particle in particles:
        psystem.add_particle_to_system(particle)
    for goal in constraints:
        psystem.add_goal_to_system(goal)

    psystem.solve(max_iter=10000, parallel=parallel)
    print(psystem.particle_positions)

cProfile.run('create_sample_system(False)')

