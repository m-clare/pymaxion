from pymaxion.particle_system import ParticleSystem
from pymaxion.particle import Particle
from pymaxion.goals.anchor import Anchor
from pymaxion.goals.cable import Cable
from pymaxion.goals.bar import Bar
from pymaxion.goals.force import Force

from numpy import pi

pt0 = Particle(0, 0, 0)
pt1 = Particle(0, 1, 0)
pt2 = Particle(0, 2, 0)
# pt3 = Particle(0.001, 0, 0)

# # System with 3 unique particles
# plist_1 = [pt0, pt1, pt2]
# system_1 = ParticleSystem()
# for pt in plist_1:
#     system_1.add_particle_to_system(pt)
# print('System 1:')
# print(system_1.n_particles)

# # System with 3 particles, 2 unique
# plist_2 = [pt0, pt1, pt3]
# system_2 = ParticleSystem(tol=1e-2)
# for pt in plist_2:
#     system_2.add_particle_to_system(pt)
# print('System 2:')
# print(system_2.n_particles)
# print(system_2.ref_positions)
# print(system_2.ref_particles)

# System with 2 original particles,
# one added unique Anchor, one existing Anchor
# print("From particle")
# a1 = Anchor([pt2], strength=1e10, anchor_pt=[2, 0, 10])
# a2 = Anchor.from_pt([0, 0, 0], 1e10)
# f1 = Force([pt2], [0, 0, -1e10])
# plist_3 = [pt0, pt1]
# glist_3 = [a1, a2, f1]
# system_3 = ParticleSystem()
# for pt in plist_3:
#     system_3.add_particle_to_system(pt)
# for goal in glist_3:
#     system_3.add_goal_to_system(goal)

# system_3.solve(max_iter=1000)
# print(system_3.num_iter)
# print(system_3.particle_positions)

# System with 3 particles, 2 cables, two Anchors, one Force
plist_4 = [pt0, pt1, pt2]
a1 = Anchor([pt2], strength=1e20)
a2 = Anchor.from_pt([0, 0, 0], 1e20)
E = 210000
A = 20 ** 2.0 * pi / 4.0
load = -1e6
c1 = Cable([pt0, pt1], E, A)
c2 = Cable([pt1, pt2], E, A)
f1 = Force([pt1], [0, 0, load])
glist_4 = [a1, a2, c1, c2, f1]
system_4 = ParticleSystem()
for pt in plist_4:
    system_4.add_particle_to_system(pt)
for goal in glist_4:
    system_4.add_goal_to_system(goal)

for goal in system_4.ref_goals:
    print(goal.particle_index)
    print(goal.strength)
print(system_4.particle_positions)

system_4.solve(max_iter=1000)
print(system_4.particle_positions)

