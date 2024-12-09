# Copyright (C) 2023, Princeton University.
# This source code is licensed under the BSD 3-clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Karhan Kayan

import numpy as np

from infinigen.core import surface
from infinigen.core.nodes.node_wrangler import Nodes
from infinigen.core.util.random import random_color_neighbour


def smoke_material(nw):
    # Code generated using version 2.3.2 of the node_transpiler

    principled_volume = nw.new_node(
        Nodes.PrincipledVolume,
        input_kwargs={
            "Color": random_color_neighbour((0.3803, 0.3803, 0.3803, 1.0)),
            "Density": np.random.uniform(1.0, 5.0),
        },
    )

    material_output = nw.new_node(
        Nodes.MaterialOutput, input_kwargs={"Volume": principled_volume}
    )


def apply(obj, selection=None, **kwargs):
    surface.add_material(obj, smoke_material, selection=selection)
