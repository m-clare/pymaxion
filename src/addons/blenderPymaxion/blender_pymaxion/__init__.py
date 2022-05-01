import os
import sys
import json

bpy = sys.modules.get("bpy")

if bpy is not None:
    import bpy
    from bpy.utils import register_class
    from bpy.utils import unregister_class
    from bpy.types import PropertyGroup
    from bpy.props import FloatProperty
    from bpy.props import IntProperty
    from bpy.props import StringProperty
    from bpy.props import PointerProperty

    # Check if this add-on is being reloaded
    if "ui" not in locals():
        from . import ui
        from . import operator
    else:
        import importlib
        ui = importlib.reload(ui)
        operator = importlib.reload(operator)
        properties = importlib.reload(properties)

    classes = (
        operator.create_particle_system,
        operator.solve_particle_system,
        operator.write_particle_system,
        operator.reset_particle_system,
        operator.PYMAXION_OT_anchorConstraint,
        operator.PYMAXION_OT_cableConstraint,
        operator.PYMAXION_OT_forceConstraint,
        operator.PYMAXION_OT_barConstraint,
        ui.PYMAXION_PT_particleSystem,
        ui.PYMAXION_PT_constraints,
        ui.PYMAXION_PT_Anchor,
        ui.PYMAXION_PT_Force,
        ui.PYMAXION_PT_Cable,
        ui.PYMAXION_PT_Bar,
    )

    bpy.propertyGroups = {}

    def register():
        for cls in classes:
            register_class(cls)

        # Load custom property groups from json
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/assets/property_groups.json', 'r') as f:
            properties = json.load(f)

        for groupName, attributeDefinitions in properties.items():
            attributes = {}
            for attributeDefinition in attributeDefinitions:
                attType = attributeDefinition['type']
                attName = attributeDefinition['name']
                # Note: type of attribute must be removed for class
                if attType == 'float':
                    attributeDefinition.pop('type')
                    attributes[attName] = FloatProperty(**attributeDefinition)
                elif attType == 'int':
                    attributeDefinition.pop('type')
                    attributes[attName] = IntProperty(**attributeDefinition)
                else:
                    raise TypeError('Unsupported type (%s) for %s on %s!' % (attType, attName, groupName))
            propertyGroupClass = type(groupName, (PropertyGroup,), {'__annotations__': attributes})
            bpy.utils.register_class(propertyGroupClass)
            setattr(bpy.types.Scene, groupName, PointerProperty(type=propertyGroupClass))
            bpy.propertyGroups[groupName] = propertyGroupClass

    def unregister():
        for cls in reversed(classes):
            unregister_class(cls)

        try:
            for key, value in bpy.propertyGroups.items():
                delattr(bpy.types.Object, key)
                unregister_class(value)
        except UnboundLocalError:
            pass

        bpy.samplePropertyGroups = {}
