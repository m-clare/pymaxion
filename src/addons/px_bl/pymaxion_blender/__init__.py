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
        operator.PYMAXION_OT_anchorGoal,
        operator.PYMAXION_OT_cableGoal,
        ui.PYMAXION_PT_particleSystem,
        ui.PYMAXION_PT_goals,
    )

    def register():
        for cls in classes:
            register_class(cls)

    def un_register():
        for cls in reversed(classes):
            unregister_class(cls)
