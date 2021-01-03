import sys

bpy = sys.modules.get("bpy")

if bpy is not None:
    import bpy
    from bpy.utils import register_class
    from bpy.utils import unregister_class

    from . import ui
    from . import operator

    classes = (
        operator.create_particle_system,
        ui.PYMAXION_PT_particleSystem,
    )

    def register():
        for cls in classes:
            register_class(cls)

    def un_register():
        for cls in classes:
            unregister_class(cls)
