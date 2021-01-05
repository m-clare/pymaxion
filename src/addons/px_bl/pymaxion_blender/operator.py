import bpy
from bpy.types import Operator

class create_particle_system(Operator):
    bl_idname = "pymaxion_blender.create_particle_system"
    bl_label = "Create Particle System"
    def execute(self, context):
        obj = bpy.context.active_object
        if obj.type == 'MESH':
            print("YAY A MESH!")
        else:
            raise TypeError("Particle System must come from a mesh.")
        return {'FINISHED'}

    # @staticmethod
    # def from_mesh(context):
        # pass


# class PYMAXION_OT_anchorGoal(Operator):

#     @staticmethod
#     def add_anchor(context):
#         pass

#     @staticmethod
#     def remove_anchor(context):
#         pass
#     pass

# class PYMAXION_OT_cableGoal(Operator):

#     @staticmethod
#     def add_cable(context):
#         pass

#     @staticmethod
#     def remove_cable(context):
#         pass
#     pass

# class PYMAXION_OT_forceGoal(Operator):

#     @staticmethod
#     def add_force(context):
#         pass

#     @staticmethod
#     def remove_force(context):
#         pass
#     pass

