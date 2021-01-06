import bpy
from bpy.props import EnumProperty 
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


class PYMAXION_OT_anchorGoal(Operator):
    bl_idname = 'pymaxion_blender.anchor_goal'
    bl_label = 'Anchor Goal'
    bl_description = 'Actions related to anchor goals.'
    bl_options = {'REGISTER', 'UNDO'}

    action: EnumProperty(
        items=[
            ('ADD', 'add anchors', 'add anchors'),
            ('REMOVE', 'remove anchors', 'remove anchors')
        ]
    )

    def execute(self, context):
        if self.action == 'ADD':
            self.add_anchors(context=context)
        if self.action == 'REMOVE':
            self.remove_anchors(context=context)
        return {'FINISHED'}

    @staticmethod
    def add_anchors(context):
        print("Adding anchors")

    @staticmethod
    def remove_anchors(context):
        print("Removing anchors")

class PYMAXION_OT_cableGoal(Operator):
    bl_idname = 'pymaxion_blender.cable_goal'
    bl_label = 'Cable Goal'
    bl_description = 'Actions related to cable goals.'
    bl_options = {'REGISTER', 'UNDO'}

    action: EnumProperty(
        items=[
            ('ADD', 'add cables', 'add cables'),
            ('REMOVE', 'remove cables', 'remove cables')
        ]
    )

    def execute(self, context):
        if self.action == 'ADD':
            self.add_cables(context=context)
        if self.action == 'REMOVE':
            self.remove_cables(context=context)
        return {'FINISHED'}

    @staticmethod
    def add_cables(context):
        print("Adding cables")

    @staticmethod
    def remove_cables(context):
        print("Removing cables")


# class PYMAXION_OT_forceGoal(Operator):

#     @staticmethod
#     def add_forces(context):
#         pass

#     @staticmethod
#     def remove_forces(context):
#         pass
#     pass

