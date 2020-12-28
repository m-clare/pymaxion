from pymaxion.particle_system import ParticleSystem
from pymaxion.particle import Particle
from pymaxon
psystem = ParticleSystem()

pt0 = Particle(1, 1, 1)
pt1 = Particle(1, 1.1, 1.00099)
pt2 = Particle(2, 1, 1)

pt_list = [pt0, pt1, pt2]
for particle in pt_list:
    psystem.add_particle_to_system(particle)

print(psystem.n_particles)
