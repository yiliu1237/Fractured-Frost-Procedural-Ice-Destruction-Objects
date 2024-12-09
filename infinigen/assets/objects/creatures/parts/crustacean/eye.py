# Copyright (C) 2023, Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Lingjie Mei


import bpy
import numpy as np
from numpy.random import uniform

from infinigen.assets.objects.creatures.util.creature import Part, PartFactory
from infinigen.assets.utils.object import join_objects, new_icosphere, origin2leftmost
from infinigen.core.placement.detail import remesh_with_attrs


class CrustaceanEyeFactory(PartFactory):
    tags = ["eye"]
    min_spike_distance = 0.05
    min_spike_radius = 0.02

    def make_part(self, params) -> Part:
        length = params["length"]
        sphere = new_icosphere(radius=params["radius"])
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.01, depth=length, location=(-length / 2, 0, 0)
        )
        cylinder = bpy.context.active_object
        cylinder.rotation_euler[1] = np.pi / 2
        obj = join_objects([sphere, cylinder])
        remesh_with_attrs(obj, 0.005)
        origin2leftmost(obj)

        skeleton = np.zeros((2, 3))
        skeleton[1, 0] = length
        return Part(skeleton, obj)

    def sample_params(self):
        radius = uniform(0.015, 0.02)
        length = radius * uniform(1, 1.5)
        return {"radius": radius, "length": length}
