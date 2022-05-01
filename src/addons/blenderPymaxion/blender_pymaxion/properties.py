import bpy
from bpy.types import PropertyGroup
from bpy.props import FloatProperty
from bpy.props import IntProperty
from bpy.props import StringProperty

class ScientificNotation(PropertyGroup):
    def __init__(self, num_dict={}, power_dict={}):
        self.num_dict = num_dict
        self.power_dict = power_dict
        self.number = FloatProperty()
        self.power = IntProperty()
        self.value = self.get_num()

    def get_num(self):
        default_num = {'min': -10, 'max': 10, 'default': 1, 'precision': 2}
        default_pow = {'min': -30, 'max': 30, 'default': 1}

        for key in default_num.keys():
            self.number[key] = self.num_dict.get(key, default_num[key])
            for key in default_pow.keys():
                self.power[key] = self.power_dict.get(key, default_pow[key])
        return self.number * pow(10, self.power)

class ConstraintProperties(PropertyGroup):
    def get_num(base, orderTen):
        return base * pow(10, orderTen)

    # Anchor constraint
    anchor_base: FloatProperty(min=1, max=10, default=1, precision=2)
    anchor_power: IntProperty(min=-30, max=30, default=20)
    anchor_strength = property(get_num(anchor_base, anchor_power))

    # Cable constraint
    cable_base: FloatProperty(min=1, max=10, default=1, precision=2)
    cable_power: IntProperty(min=-20, max=20, default=6)
    cable_modulus = property(get_num(cable_base, cable_power))
    cable_diameter: FloatProperty(name="Cable diameter (m)",
                                  description="Diameter of Cable",
                                  min=1e-3,
                                  max=2,
                                  default=0.05,
                                  precision=3)

    # Bar constraint
    bar_base: FloatProperty(min=1, max=10, default=1, precision=2)
    bar_power: IntProperty(min=-20, max=20, default=6)
    bar_modulus = property(get_num(bar_base, bar_power))
    bar_area: FloatProperty(name="Bar area (m^2)",
                            description="Area of Bar",
                            min=1e-3,
                            max=10,
                            default=0.05,
                            precision=3)

    # Force constraint
    force_base: FloatProperty(min=1, max=10, default=1, precision=2)
    force_power: IntProperty(min=-20, max=20, default=6)
    force_resultant = property(get_num(force_base, force_power))

