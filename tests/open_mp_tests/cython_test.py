from pymaxion.particle_system import ParticleSystem
from pymaxion.particle import Particle
from pymaxion.constraints.cable import Cable
from pymaxion.constraints.anchor import Anchor
from pymaxion.constraints.force import Force
import json
import os

BASE_FOLDER = os.path.dirname(__file__)


def run_system():
    fp = os.path.join(BASE_FOLDER, "ParticleSystem.json")
    psystem = ParticleSystem.from_json(fp)
    psystem.solve(ke=1e-10, max_iter=10000)
    print(psystem.num_iter)


if __name__ == "__main__":
    run_system()
