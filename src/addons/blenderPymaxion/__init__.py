bl_info = {
    "name": "Pymaxion",
    "description": "Projection based physics simulator/geometric constraint solver",
    "author": "Maryanne Wachter",
    "blender": (3, 1, 0),
    "version": (0, 0, 1),
    "location": "Scene / Object / Mesh Properties",
    "category": "Object"
}

# General import - no file structure yet
from .blender_pymaxion import *

if __name__ == "__main__":
    register()
