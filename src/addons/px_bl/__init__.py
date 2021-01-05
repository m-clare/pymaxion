bl_info = {
    "name": "Pymaxion",
    "description": "DR based physics simulator/geometric constraint solver",
    "author": "Maryanne Wachter",
    "blender": (2, 91, 0),
    "version": (0, 0, 1),
    "location": "Scene / Object / Mesh Properties",
    "category": "Object"
}

# General import - no file structure yet
from .pymaxion_blender import *

if __name__ == "__main__":
    register()

