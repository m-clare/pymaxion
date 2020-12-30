from pymaxion.particle_system import ParticleSystem
from pymaxion.particle import Particle
from pymaxion.goals.anchor import Anchor
from pymaxion.goals.cable import Cable
from pymaxion.goals.goal import Goal
# from pymaxion.goals.force import Force


pt0 = Particle(0, 0, 0)
pt1 = Particle(0, 1, 0)
pt2 = Particle(0, 2, 0)
pt3 = Particle(0.001, 0, 0)
print(type(pt3))

# # System with 3 unique particles
# plist_1 = [pt0, pt1, pt2]
# system_1 = ParticleSystem()
# for pt in plist_1:
#     system_1.add_particle_to_system(pt)
# print(system_1.n_particles)

# # System with 3 particles, 2 unique
# plist_2 = [pt0, pt1, pt3]
# system_2 = ParticleSystem(tol=1e-2)
# for pt in plist_2:
#     system_2.add_particle_to_system(pt)
# print(system_2.n_particles)
# print(system_2.ref_positions)
# print(system_2.ref_particles)

# System with 2 original particles,
# one added unique Anchor, one existing Anchor
# g1 = Goal([pt0])
# g2 = Anchor([pt0], strength=1e10)
# print(g1.particles)
# print(g1.particles[0].sum_weights)
g2 = Anchor([pt0])
# a1 = Anchor([pt2], strength=1e10)# print(type(a1.particles))# a2 = Anchor([0, 0, 0], strength=1e10)
# plist_3 = [pt0, pt1]
# glist_3 = [a1, a2]
# system_3 = ParticleSystem()
# for pt in plist_3:
#     system_3.add_particle_to_system(pt)
# for goal in glist_3:
#     system_3.add_goal_to_system(goal)
# print(system_3.n_particles)
# for goal in system_3.ref_goals:
#     print(goal.particles)
#     print(goal.particle_index)

# System with 3 particles, 2 cables, two Anchors, one Force
