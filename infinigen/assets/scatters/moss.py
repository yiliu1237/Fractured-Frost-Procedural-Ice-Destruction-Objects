# Copyright (C) 2023, Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Lingjie Mei

import numpy as np
from numpy.random import uniform as U

from infinigen.assets.objects.particles import MossFactory
from infinigen.assets.utils.misc import assign_material
from infinigen.core import surface
from infinigen.core.nodes.node_wrangler import Nodes, NodeWrangler
from infinigen.core.placement.factory import make_asset_collection
from infinigen.core.placement.instance_scatter import scatter_instances


class MossCover:
    def __init__(self):
        self.col = make_asset_collection(
            MossFactory(np.random.randint(1e5)), name="moss", n=3
        )
        base_hue = U(0.24, 0.28)
        for o in self.col.objects:
            assign_material(
                o,
                surface.shaderfunc_to_material(
                    MossFactory.shader_moss, (base_hue + U(-0.02, 0.02)) % 1
                ),
            )

    def apply(self, obj, selection=None):
        def instance_index(nw: NodeWrangler, n):
            return nw.math(
                "MODULO",
                nw.new_node(
                    Nodes.FloatToInt, [nw.scalar_multiply(nw.musgrave(10), 2 * n)]
                ),
                n,
            )

        scatter_obj = scatter_instances(
            base_obj=obj,
            collection=self.col,
            density=2e4,
            min_spacing=0.005,
            scale=1,
            scale_rand=U(0.3, 0.7),
            selection=selection,
            instance_index=instance_index,
        )

        return scatter_obj


def apply(obj):
    moss_cover = MossCover()
    return moss_cover.apply(obj)
