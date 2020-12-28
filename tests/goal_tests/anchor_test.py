from pymaxion.goals.anchor import Anchor
from pymaxion.particle_system import ParticleSystem
from pymaxion.geometry.Point3d cimport Point3d


pt0 = Anchor([1.0, 1.0, 1.0], 10.0)
pt1 = Anchor([1.0, 2.0, 2.0], 10.0)

psystem = ParticleSystem()

psystem.add_goal_to_system(pt0)
psystem.add_goal_to_system(pt1)

