import bpy
from bpy.props import EnumProperty 
from bpy.types import Operator
import bmesh
import sys

sys.path.append('/Users/maryannewachter/workspaces/current/pymaxion/src')

# Pymaxion imports
from pymaxion.goals.anchor import Anchor
from pymaxion.particle_system import ParticleSystem
from pymaxion.particle import Particle
from pymaxion.goals.cable import Cable
from pymaxion.goals.force import Force

class create_particle_system(Operator):
    bl_idname = 'pymaxion_blender.create_particle_system'
    bl_label = 'Create Particle System'
    def execute(self, context):
        obj = bpy.context.active_object
        if obj.type == 'MESH':
            obj.name = 'Pymaxion Particle System'
            obj.data['ParticleSystem'] = {'Anchors': [],
                                          'Cables': [],
                                          'Forces': []}
        else:
            raise TypeError('Particle System must come from a mesh.')
        return {'FINISHED'}

class solve_particle_system(Operator):
    bl_idname = 'pymaxion_blender.solve_particle_system'
    bl_label = 'Solve Particle System'

    def execute(self, context):
        # check if particle system mesh exists

        psystem = ParticleSystem()
        return {'FINISHED'}
        



class PYMAXION_OT_anchorGoal(Operator):
    bl_idname = 'pymaxion_blender.anchor_goal'
    bl_label = 'Anchor Goal'
    bl_description = 'Actions related to anchor goals.'
    bl_options = {'REGISTER', 'UNDO'}

    action: EnumProperty(
        items=[
            ('ADD', 'add anchors', 'add anchors'),
            ('REMOVE', 'remove anchors', 'remove anchors'),
            ('SHOW', 'show anchors', 'show anchors')
        ]
    )

    def execute(self, context):
        if self.action == 'ADD':
            self.add_anchors(context=context)
        if self.action == 'REMOVE':
            self.remove_anchors(context=context)
        if self.action == 'SHOW':
            self.show_anchors(context=context)
        return {'FINISHED'}

    @staticmethod
    def add_anchors(context):
        obj = bpy.context.active_object
        if obj.type == 'MESH':
            if obj.name == 'Pymaxion Particle System':
                ps = obj.data['ParticleSystem']
                for v in obj.data.vertices:
                    if v.select:
                        print(v.index)
                        ps['Anchors'].append({'m_index': v.index,
                                              'strength': 1e20})
            else:
                raise ValueError('Anchors are not part of a Pymaxion Particle System')

        print('Adding anchors')

    @staticmethod
    def remove_anchors(context):
        print('Removing anchors')

    @staticmethod
    def show_anchors(context):
        print('Showing anchors')

class PYMAXION_OT_cableGoal(Operator):
    bl_idname = 'pymaxion_blender.cable_goal'
    bl_label = 'Cable Goal'
    bl_description = 'Actions related to cable goals.'
    bl_options = {'REGISTER', 'UNDO'}

    action: EnumProperty(
        items=[
            ('ADD', 'add cables', 'add cables'),
            ('REMOVE', 'remove cables', 'remove cables'),
            ('SHOW', 'show cables', 'show cables')
        ]
    )

    def execute(self, context):
        if self.action == 'ADD':
            self.add_cables(context=context)
        if self.action == 'REMOVE':
            self.remove_cables(context=context)
        if self.action == 'SHOW':
            self.show_cables(context=context)
        return {'FINISHED'}

    @staticmethod
    def add_cables(context):
        obj = bpy.context.active_object
        if obj.type == 'MESH':
            if obj.name == 'Pymaxion Particle System':
                ps = obj.data['ParticleSystem']
                for e in obj.data.edges:
                    if e.select:
                        vs = edge.vertices
                        ps['Cables'].append({'m_index': [vs[0], vs[1]],
                                             'E': 210e9,
                                             'A': 0.02 ** 2.0 * np.pi / 4.0})
            else:
                raise ValueError('Cables are not part of a Pymaxion Particle System')
        print('Adding cables')

    @staticmethod
    def remove_cables(context):
        print('Removing cables')

    @staticmethod
    def show_cables(context):
        print('Showing cables')


class PYMAXION_OT_forceGoal(Operator):
    bl_idname = 'pymaxion_blender.force_goal'
    bl_label = 'Force Goal'
    bl_description = 'Actions related to point force goals.'
    bl_options = {'REGISTER', 'UNDO'}

    action: EnumProperty(
        items=[
            ('ADD', 'add force', 'add force'),
            ('REMOVE', 'remove force', 'remove force'),
            ('SHOW', 'show force', 'show force')
        ]
    )

    def execute(self, context):
        if self.action == 'ADD':
            self.add_forces(context=context)
        if self.action == 'REMOVE':
            self.remove_forces(context=context)
        if self.action == 'SHOW':
            self.show_forces(context=context)
        return {'FINISHED'}

    @staticmethod
    def add_forces(context):
        obj = bpy.context.active_object
        if obj.type == 'MESH':
            if obj.name == 'Pymaxion Particle System':
                for v in obj.data.verticess:
                    if v.select:
                        ps['Anchor'].append({'m_index': v.index,
                                             'vector': [0, 0, -5e6]})          
            else:
                raise ValueError('Force application points ' +
                                 'are not part of a Pymaxion Particle System')

    @staticmethod
    def remove_forces(context):
        print('Removing forces')

    @staticmethod
    def show_forces(context):
        print('Showing forces')

# class PYMAXION_OT_forceGoal(Operator):

#     @staticmethod
#     def add_forces(context):
#         pass

#     @staticmethod
#     def remove_forces(context):
#         pass
#     pass

