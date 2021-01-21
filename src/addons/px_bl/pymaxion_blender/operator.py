import bpy
from bpy.props import EnumProperty 
from bpy.types import Operator
import bmesh
import sys
import numpy as np
from profilehooks import profile
import json

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
        else:
            raise TypeError('Particle System must come from a mesh.')
        return {'FINISHED'}

class write_particle_system(Operator):
    bl_idname = 'pymaxion_blender.write_particle_system'
    bl_label = 'Write Particle System'

    def execute(self, context):
        data = {} # for json
        obj = bpy.data.objects['Pymaxion Particle System']
        me = obj.data

        data['Particles'] = []
        for index, v in enumerate(me.vertices):
            data['Particles'].append([v.co.x, v.co.y, v.co.z])

        data['Cables'] = {}
        if obj.data['Cables']:
            for cable, attr in obj.data['Cables'].items():
                strength = attr['E'] * attr['A']
                data['Cables'].update({cable: strength})
        data['Anchors'] = {}
        if obj.data['Anchors']:
            for anchor, attr in obj.data['Anchors'].items():
                strength = attr['strength']
                data['Anchors'].update({anchor: strength})
        data['Forces'] = {}
        if obj.data['Forces']:
            for force, attr in obj.data['Forces'].items():
                vector = attr['vector']
                data['Forces'].update({force: [vector[0], vector[1], vector[2]]})

        with open("ParticleSystem.json", 'w+') as f:
            json.dump(data, f, sort_keys=True, indent=4)

        return {'FINISHED'}

class solve_particle_system(Operator):
    bl_idname = 'pymaxion_blender.solve_particle_system'
    bl_label = 'Solve Particle System'

    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")

    def execute(self, context):
        if bpy.data.objects['Pymaxion Particle System']:
            obj = bpy.data.objects['Pymaxion Particle System']
            print("Found particle system!")

            data = self.profile_run(obj)

        return {'FINISHED'}

    @profile
    def profile_run(self, obj):
        me = obj.data
        psystem = ParticleSystem()

        for pt in obj.data.vertices:
            x, y, z = self.get_vert_coordinates(pt.index)
            psystem.add_particle_to_system(Particle(x, y, z))

        if obj.data['Cables']:
            cables = self.parse_cables(obj.data['Cables'])
            psystem.add_goals_to_system(cables)

        if obj.data['Forces']:
            forces = self.parse_forces(obj.data['Forces'])
            psystem.add_goals_to_system(forces)

        if obj.data['Anchors']:
            anchors = self.parse_anchors(obj.data['Anchors'])
            psystem.add_goals_to_system(anchors)

        bpy.ops.object.mode_set(mode='OBJECT')

        psystem.solve(max_iter=100000, ke=1e-15, parallel=False)
        print(psystem.num_iter)

        data = psystem.particle_positions

        for index, v in enumerate(me.vertices):
            v.co = data[index]

        return data

    def get_vert_coordinates(self, vert_index):
        obj = bpy.data.objects['Pymaxion Particle System']
        verts = obj.data.vertices
        x, y, z = verts[vert_index].co
        return x, y, z

    def parse_cables(self, cables):
        cable_list = []
        for cable, attr in cables.items():
            ct = eval(cable)
            x0, y0, z0 = self.get_vert_coordinates(ct[0])
            x1, y1, z1 = self.get_vert_coordinates(ct[1])
            p0 = Particle(x0, y0, z0)
            p1 = Particle(x1, y1, z1)
            pcable = Cable([p0, p1], attr['E'], attr['A'])
            cable_list.append(pcable)
        return cable_list

    def parse_anchors(self, anchors):
        anchor_list = []
        for anchor, attr in anchors.items():
            at = eval(anchor)
            x0, y0, z0 = self.get_vert_coordinates(at)
            p0 = Particle(x0, y0, z0)
            panchor = Anchor([p0], attr['strength'])
            anchor_list.append(panchor)
        return anchor_list

    def parse_forces(self, forces):
        force_list = []
        for force, attr in forces.items():
            ft = eval(force)
            x0, y0, z0 = self.get_vert_coordinates(ft)
            p0 = Particle(x0, y0, z0)
            vec = attr['vector']
            pforce = Force([p0], [vec[0], vec[1], vec[2]])
            force_list.append(pforce)
        return force_list



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
                mode = bpy.context.active_object.mode
                bpy.ops.object.mode_set(mode='OBJECT')
                vs = [v for v in bpy.context.active_object.data.vertices if v.select]
                if 'Anchors' not in obj.data:
                    obj.data['Anchors'] = {}
                for v in vs:
                    obj.data['Anchors'][str(v.index)] = {'strength': 1e20}
                    print("Added an anchor " + str(v.index))
                bpy.ops.object.mode_set(mode=mode)
            else:
                raise ValueError('Anchors are not part of a Pymaxion Particle System')

    @staticmethod
    def remove_anchors(context):
        # if bpy.data.objects['Pymaxion Particle System']:
            # obj = bpy.context.
        print('Removing anchors')

    @staticmethod
    def show_anchors(context):
        obj = bpy.data.objects['Pymaxion Particle System']
        if 'Anchors' in obj.data:
            for key, value in obj.data['Anchors'].items():
                print(key, obj.data['Anchors'][key]['strength'])
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
                mode = bpy.context.active_object.mode
                bpy.ops.object.mode_set(mode='OBJECT')
                es = [e for e in bpy.context.active_object.data.edges if e.select]
                if 'Cables' not in obj.data:
                    obj.data['Cables'] = {}
                for e in es:
                    vs = e.vertices
                    obj.data['Cables'][str((vs[0], vs[1]))] = {'E': 210e9,
                                                               'A': 0.02 ** 2.0 * np.pi / 4.0}
                    print("Added a cable " + str((vs[0], vs[1])))
                bpy.ops.object.mode_set(mode=mode)
            else:
                raise ValueError('Cables are not part of a Pymaxion Particle System')

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
                mode = bpy.context.active_object.mode
                bpy.ops.object.mode_set(mode='OBJECT')
                vs = [v for v in bpy.context.active_object.data.vertices if v.select]
                if 'Forces' not in obj.data:
                    obj.data['Forces'] = {}
                for v in vs:
                    obj.data['Forces'][str(v.index)] = {'vector': [0, 0, -5e6]}
                    print("Added a force " + str(v.index))
                bpy.ops.object.mode_set(mode=mode)
            else:
                raise ValueError('Forces are not part of a Pymaxion Particle System')


    @staticmethod
    def remove_forces(context):
        print('Removing forces')

    @staticmethod
    def show_forces(context):
        print('Showing forces')


