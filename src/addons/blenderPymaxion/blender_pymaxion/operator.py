import bpy
from bpy.props import EnumProperty
from bpy.types import Operator
import bmesh
import sys
import numpy as np
# from profilehooks import profile
import json
from math import pi

# Pymaxion imports
from pymaxion.constraints.anchor import Anchor
from pymaxion.particle_system import ParticleSystem
from pymaxion.particle import Particle
from pymaxion.constraints.cable import Cable
from pymaxion.constraints.force import Force
from pymaxion.constraints.bar import Bar


class create_particle_system(Operator):
    bl_idname = "pymaxion_blender.create_particle_system"
    bl_label = "Create Particle System"

    def execute(self, context):
        obj = bpy.context.active_object
        if obj.type == "MESH":
            obj.name = "Pymaxion Particle System"
        else:
            raise TypeError("Particle System must come from a mesh.")
        return {"FINISHED"}


class write_particle_system(Operator):
    bl_idname = "pymaxion_blender.write_particle_system"
    bl_label = "Write Particle System"

    def execute(self, context):
        data = {}  # for json
        obj = bpy.data.objects["Pymaxion Particle System"]
        me = obj.data

        data["Particles"] = []
        for index, v in enumerate(me.vertices):
            data["Particles"].append([v.co.x, v.co.y, v.co.z])
        # TODO: add prestressed length
        # TODO: General writing attr based on available obj data
        data["Cables"] = {}
        if "Cables" in obj.data:
            for cable, attr in obj.data["Cables"].items():
                E = attr["E"]
                A = attr["A"]
                data["Cables"].update({cable: {"E": E, "A": A}})
        data["Bars"] = {}
        if "Bars" in obj.data:
            for bar, attr in obj.data["Bars"].items():
                E = attr["E"]
                A = attr["A"]
                data["Bars"].update({bar: {"E": E, "A": A}})
        data["Anchors"] = {}
        if "Anchors" in obj.data:
            for anchor, attr in obj.data["Anchors"].items():
                strength = attr["strength"]
                data["Anchors"].update({anchor: {"strength": strength}})
        data["Forces"] = {}
        if "Forces" in obj.data:
            for force, attr in obj.data["Forces"].items():
                vector = attr["vector"]
                data["Forces"].update({force: [vector[0], vector[1], vector[2]]})

        with open("ParticleSystem.json", "w+") as f:
            json.dump(data, f, sort_keys=True, indent=4)

        return {"FINISHED"}


class solve_particle_system(Operator):
    bl_idname = "pymaxion_blender.solve_particle_system"
    bl_label = "Solve Particle System"

    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")

    def execute(self, context):
        if bpy.data.objects["Pymaxion Particle System"]:
            obj = bpy.data.objects["Pymaxion Particle System"]
            bpy.context.view_layer.objects.active = obj
            new_obj = obj.copy()
            new_obj.data = obj.data.copy()
            obj.name = "Pymaxion Initial Particle System"
            new_obj.name = "Pymaxion Particle System"
            bpy.context.collection.objects.link(new_obj)
            obj.hide_set(True)
            print("Found particle system!")
            data = self.profile_run(new_obj)

        return {"FINISHED"}

    # @profile
    def profile_run(self, obj):
        me = obj.data
        psystem = ParticleSystem()

        for pt in obj.data.vertices:
            x, y, z = self.get_vert_coordinates(obj, pt.index)
            psystem.add_particle_to_system(Particle(x, y, z))

        # TODO: Generalize constraint types so that "parse" will match to the correct function?
        if "Cables" in obj.data:
            cables = self.parse_cables(obj, obj.data["Cables"])
            psystem.add_constraints_to_system(cables)

        if "Bars" in obj.data:
            bars = self.parse_bars(obj, obj.data["Bars"])
            psystem.add_constraints_to_system(bars)

        if "Forces" in obj.data:
            forces = self.parse_forces(obj, obj.data["Forces"])
            psystem.add_constraints_to_system(forces)

        if "Anchors" in obj.data:
            anchors = self.parse_anchors(obj ,obj.data["Anchors"])
            psystem.add_constraints_to_system(anchors)

        bpy.ops.object.mode_set(mode="OBJECT")

        psystem.solve(max_iter=100000, ke=1e-10, parallel=False)
        print(psystem.num_iter)

        data = psystem.particle_positions

        for index, v in enumerate(me.vertices):
            v.co = data[index]

        return data

    def get_vert_coordinates(self, obj, vert_index):
        verts = obj.data.vertices
        x, y, z = verts[vert_index].co
        return x, y, z

    def parse_cables(self, obj, cables):
        cable_list = []
        for cable, attr in cables.items():
            ct = eval(cable)
            x0, y0, z0 = self.get_vert_coordinates(obj, ct[0])
            x1, y1, z1 = self.get_vert_coordinates(obj, ct[1])
            p0 = Particle(x0, y0, z0)
            p1 = Particle(x1, y1, z1)
            pcable = Cable([p0, p1], attr["E"], attr["A"])
            cable_list.append(pcable)
        return cable_list

    def parse_bars(self, obj, bars):
        bar_list = []
        for bar, attr in bars.items():
            bt = eval(bar)
            x0, y0, z0 = self.get_vert_coordinates(obj, bt[0])
            x1, y1, z1 = self.get_vert_coordinates(obj, bt[1])
            p0 = Particle(x0, y0, z0)
            p1 = Particle(x1, y1, z1)
            pbar = Bar([p0, p1], attr["E"], attr["A"])
            bar_list.append(pbar)

    def parse_anchors(self, obj, anchors):
        anchor_list = []
        for anchor, attr in anchors.items():
            at = eval(anchor)
            x0, y0, z0 = self.get_vert_coordinates(obj, at)
            p0 = Particle(x0, y0, z0)
            panchor = Anchor([p0], attr["strength"])
            anchor_list.append(panchor)
        return anchor_list

    def parse_forces(self, obj, forces):
        force_list = []
        for force, attr in forces.items():
            ft = eval(force)
            x0, y0, z0 = self.get_vert_coordinates(obj, ft)
            p0 = Particle(x0, y0, z0)
            vec = attr["vector"]
            pforce = Force([p0], [vec[0], vec[1], vec[2]])
            force_list.append(pforce)
        return force_list


class reset_particle_system(Operator):
    bl_idname = "pymaxion_blender.reset_particle_system"
    bl_label = "Reset Particle System"

    def execute(self, context):
        # check if updated and initial systems exist
        if bpy.data.objects["Pymaxion Initial Particle System"] and bpy.data.objects["Pymaxion Particle System"]:
            # "archive existing system" -- set up as User choice?
            archive_obj = bpy.data.objects["Pymaxion Particle System"]
            archive_obj.name = "pps_archived"
            # remove object from collection
            bpy.data.objects.remove(archive_obj)
            reset_obj = bpy.data.objects["Pymaxion Initial Particle System"]
            reset_obj.name = "Pymaxion Particle System"
            reset_obj.hide_set(False)
        else:
            raise ValueError("No sufficient particle system found.")

        return {"FINISHED"}


class PYMAXION_OT_anchorConstraint(Operator):
    bl_idname = "pymaxion_blender.anchor_constraint"
    bl_label = "Anchor Constraint"
    bl_description = "Actions related to anchor constraints."
    bl_options = {"REGISTER", "UNDO"}

    action: EnumProperty(
        items=[
            ("ADD", "add anchors", "add anchors"),
            ("REMOVE", "remove anchors", "remove anchors"),
            ("SHOW", "show anchors", "show anchors"),
        ]
    )

    def execute(self, context):
        scene = context.scene
        tools = scene.tools
        if self.action == "ADD":
            self.add_anchors(context=context, strength=tools.anchor_strength)
        if self.action == "REMOVE":
            self.remove_anchors(context=context)
        if self.action == "SHOW":
            self.show_anchors(context=context)
        return {"FINISHED"}

    @staticmethod
    def add_anchors(context, strength):
        obj = bpy.context.active_object
        if obj.type == "MESH":
            if obj.name == "Pymaxion Particle System":
                mode = bpy.context.active_object.mode
                bpy.ops.object.mode_set(mode="OBJECT")
                vs = [v for v in bpy.context.active_object.data.vertices if v.select]
                if "Anchors" not in obj.data:
                    obj.data["Anchors"] = {}
                for v in vs:
                    obj.data["Anchors"][str(v.index)] = {"strength": strength}
                    print("Added an anchor " + str(v.index))
                bpy.ops.object.mode_set(mode=mode)
            else:
                raise ValueError("Anchors are not part of a Pymaxion Particle System")

    @staticmethod
    def remove_anchors(context):
        obj = bpy.context.active_object
        if obj.type == "MESH":
            if obj.name == "Pymaxion Particle System":
                mode = bpy.context.active_object.mode
                bpy.ops.object.mode_set(mode="EDIT")
                vs = [v for v in bpy.context.active_object.data.vertices if v.select]
                if "Anchors" in obj.data:
                    bpy.ops.mesh.select_all(action='DESELECT')
                    for v in vs:
                        obj.data["Anchors"].pop(str(v.index), None)
                        print("Removing anchor at " + str(v.index))

    @staticmethod
    def show_anchors(context):
        if bpy.data.objects["Pymaxion Particle System"]:
            obj = bpy.data.objects['Pymaxion Particle System']
            mode = bpy.context.active_object.mode
            bpy.ops.object.mode_set(mode="OBJECT")
            if "Anchors" in obj.data:
                for key in obj.data["Anchors"].keys():
                    id = eval(key)
                    obj.data.vertices[id].select = True
                    print(key, obj.data["Anchors"][key]["strength"])
                bpy.ops.object.mode_set(mode = 'EDIT')
        print("Showing anchors")


class PYMAXION_OT_cableConstraint(Operator):
    bl_idname = "pymaxion_blender.cable_constraint"
    bl_label = "Cable Constraint"
    bl_description = "Actions related to cable constraints."
    bl_options = {"REGISTER", "UNDO"}

    action: EnumProperty(
        items=[
            ("ADD", "add cables", "add cables"),
            ("REMOVE", "remove cables", "remove cables"),
            ("SHOW", "show cables", "show cables"),
        ]
    )

    def execute(self, context):
        scene = context.scene
        tools = scene.tools
        if self.action == "ADD":
            self.add_cables(context=context, E=tools.cable_modulus, d=tools.cable_diameter)
        if self.action == "REMOVE":
            self.remove_cables(context=context)
        if self.action == "SHOW":
            self.show_cables(context=context)
        return {"FINISHED"}

    @staticmethod
    def add_cables(context, E, d):
        obj = bpy.context.active_object
        if obj.type == "MESH":
            if obj.name == "Pymaxion Particle System":
                mode = bpy.context.active_object.mode
                bpy.ops.object.mode_set(mode="OBJECT")
                es = [e for e in bpy.context.active_object.data.edges if e.select]
                if "Cables" not in obj.data:
                    obj.data["Cables"] = {}
                for e in es:
                    vs = e.vertices
                    obj.data["Cables"][str((vs[0], vs[1]))] = {
                        "E": E,
                        "A": 0.25 * d ** 2.0 * pi,
                    }
                    print("Added a cable " + str((vs[0], vs[1])))
                bpy.ops.object.mode_set(mode=mode)
            else:
                raise ValueError("Cables are not part of a Pymaxion Particle System")

    @staticmethod
    def remove_cables(context):
        print("Removing cables")

    @staticmethod
    def show_cables(context):
        print("Showing cables")


class PYMAXION_OT_barConstraint(Operator):
    bl_idname = "pymaxion_blender.bar_constraint"
    bl_label = " Constraint"
    bl_description = "Actions related to bar constraints."
    bl_options = {"REGISTER", "UNDO"}

    action: EnumProperty(
        items=[
            ("ADD", "add bars", "add bars"),
            ("REMOVE", "remove bars", "remove bars"),
            ("SHOW", "show bars", "show bars"),
        ]
    )

    def execute(self, context):
        scene = context.scene
        tools = scene.tools
        if self.action == "ADD":
            self.add_bars(context=context, E=tools.bar_modulus, A=tools.bar_area)
        if self.action == "REMOVE":
            self.remove_bars(context=context)
        if self.action == "SHOW":
            self.show_bars(context=context)
        return {"FINISHED"}

    @staticmethod
    def add_bars(context, E, A):
        obj = bpy.context.active_object
        if obj.type == "MESH":
            if obj.name == "Pymaxion Particle System":
                mode = bpy.context.active_object.mode
                bpy.ops.object.mode_set(mode="OBJECT")
                es = [e for e in bpy.context.active_object.data.edges if e.select]
                if "Bars" not in obj.data:
                    obj.data["Bars"] = {}
                for e in es:
                    vs = e.vertices
                    obj.data["Bars"][str((vs[0], vs[1]))] = {
                        "E": E,
                        "A": A,
                    }
                    print("Added a bar " + str((vs[0], vs[1])))
                bpy.ops.object.mode_set(mode=mode)
            else:
                raise ValueError("Bars are not part of a Pymaxion Particle System")

    @staticmethod
    def remove_bars(context):
        print("Removing bars")

    @staticmethod
    def show_bars(context):
        print("Showing bars")


class PYMAXION_OT_forceConstraint(Operator):
    bl_idname = "pymaxion_blender.force_constraint"
    bl_label = "Force Constraint"
    bl_description = "Actions related to point force constraints."
    bl_options = {"REGISTER", "UNDO"}

    action: EnumProperty(
        items=[
            ("ADD", "add force", "add force"),
            ("REMOVE", "remove force", "remove force"),
            ("SHOW", "show force", "show force"),
        ]
    )

    def execute(self, context):
        scene = context.scene
        sciProp = scene.sciProp
        if self.action == "ADD":
            self.add_forces(context=context, strength=sciProp.value)
        if self.action == "REMOVE":
            self.remove_forces(context=context)
        if self.action == "SHOW":
            self.show_forces(context=context)
        return {"FINISHED"}

    @staticmethod
    def add_forces(context, strength):
        obj = bpy.context.active_object
        if obj.type == "MESH":
            if obj.name == "Pymaxion Particle System":
                mode = bpy.context.active_object.mode
                bpy.ops.object.mode_set(mode="OBJECT")
                vs = [v for v in bpy.context.active_object.data.vertices if v.select]
                if "Forces" not in obj.data:
                    obj.data["Forces"] = {}
                for v in vs:
                    obj.data["Forces"][str(v.index)] = {"vector": [0, 0, strength]}
                    print("Added a force " + str(v.index))
                bpy.ops.object.mode_set(mode=mode)
            else:
                raise ValueError("Forces are not part of a Pymaxion Particle System")

    @staticmethod
    def remove_forces(context):
        print("Removing forces")

    @staticmethod
    def show_forces(context):
        print("Showing forces")
