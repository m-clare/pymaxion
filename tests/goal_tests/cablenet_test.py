# Pymaxion imports
from pymaxion.goals.anchor import Anchor
from pymaxion.particle_system import ParticleSystem
from pymaxion.particle import Particle
from pymaxion.goals.cable import Cable
from pymaxion.goals.force import Force


def create_sample_system(parallel=False):
    # initial position
    verts = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), 
             (-1, -1, 0), (0, -1, 0), (1, -1, 0), (2, -1, 0), (3, -1, 0), (4, -1, 0),
             (-1, -2, 0), (0, -2, 0), (1, -2, 0), (2, -2, 0), (3, -2, 0), (4, -2, 0),
             (-1, -3, 0), (0, -3, 0), (1, -3, 0), (2, -3, 0), (3, -3, 0), (4, -3, 0),
             (-1, -4, 0), (0, -4, 0), (1, -4, 0), (2, -4, 0), (3, -4, 0), (4, -4, 0),
             (0, -5, 0), (1, -5, 0), (2, -5, 0), (3, -5, 0)]

    edges = [(0, 5), (1, 6), (2, 7), (3, 8),
             (5, 11), (6, 12), (7, 13), (8, 14),
             (11, 17), (12, 18), (13, 19), (14, 20),
             (17, 23), (18, 24), (19, 25), (20, 26),
             (23, 28), (24, 29), (25, 30), (26, 31),
             (4, 5), (5, 6), (6, 7), (7, 8), (8, 9),
             (10, 11), (11, 12), (12, 13), (13, 14), (14, 15),
             (16, 17), (17, 18), (18, 19), (19, 20), (20, 21),
             (22, 23), (23, 24), (24, 25), (25, 26), (26, 27)]

    faces = []

    psystem = ParticleSystem()

    particles = []
    for i in range(len(verts)):
        particles.append(Particle(verts[i][0], verts[i][1], verts[i][2]))

    E = 210e9
    A = 0.02 ** 2.0 * np.pi / 4.0
    load = -5e6

    anchor_indices = [0, 1, 2, 3, 4, 9, 10, 15, 16, 21, 22, 27, 28, 29, 30, 31]
    anchors = []
    for pt in anchor_indices:
        anchors.append(Anchor.from_pt(list(verts[pt]), 1e20))

    cables = []
    for i in range(len(edges)):
        lp0 = verts[edges[i][0]]
        lp1 = verts[edges[i][1]]
        p0 = Particle(lp0[0], lp0[1], lp0[2])
        p1 = Particle(lp1[0], lp1[1], lp1[2])
        cables.append(Cable([p0, p1], E, A, 1.0))

    loads = []
    for i in range(len(verts)):
        loads.append(Force([Particle(verts[i][0], verts[i][1], verts[i][2])], [0, 0, load]))

    for anchor in anchors:
        psystem.add_goal_to_system(anchor)

    for cable in cables:
        psystem.add_goal_to_system(cable)

    for load in loads:
        psystem.add_goal_to_system(load)

    for particle in particles:
        psystem.add_particle_to_system(particle)

    psystem.solve(max_iter=100000, ke=1e-15, parallel=False)
    print(psystem.num_iter)

cProfile.run('create_sample_system(False)')
