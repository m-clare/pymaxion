import bpy
from bpy.types import Panel

class PYMAXION_PT_particleSystem(Panel):
    bl_idname = 'PYMAXION_PT_particleSystem'
    bl_label = 'Particle System'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Pymaxion'

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        op = row.operator('pymaxion_blender.create_particle_system',
                          text='Create Particle System')
        row = layout.row(align=True)
        op = row.operator('pymaxion_blender.solve_particle_system',
                          text='Solve Particle System')
        row = layout.row(align=True)
        op = row.operator('pymaxion_blender.write_particle_system',
                          text='Write Particle System')

class PYMAXION_PT_constraints(Panel):
    bl_idname = 'PYMAXION_PT_constraints'
    bl_label = 'Constraints'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Pymaxion'

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.operator('pymaxion_blender.anchor_constraint',
                     text='Add Anchors').action = 'ADD'
        row.operator('pymaxion_blender.anchor_constraint',
                     text='Remove Anchors').action = 'REMOVE'
        row.operator('pymaxion_blender.anchor_constraint',
                     text='Show Anchors').action = 'SHOW'

        row = layout.row(align=True)
        row.operator('pymaxion_blender.cable_constraint',
                     text='Add Cables').action = 'ADD'
        row.operator('pymaxion_blender.cable_constraint',
                     text='Remove Cables').action = 'REMOVE'
        row.operator('pymaxion_blender.cable_constraint',
                     text='Show Cables').action = 'SHOW'

        row = layout.row(align=True)
        row.operator('pymaxion_blender.force_constraint',
                     text='Add Forces').action = 'ADD'
        row.operator('pymaxion_blender.force_constraint',
                     text='Remove Forces').action = 'REMOVE'
        row.operator('pymaxion_blender.force_constraint',
                     text='Show Forces').action = 'SHOW'
