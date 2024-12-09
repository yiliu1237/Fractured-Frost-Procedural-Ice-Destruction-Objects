# Copyright (C) 2023, Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Lingjie Mei

import numpy as np
from numpy.random import uniform

from infinigen.assets.objects.monocot.growth import MonocotGrowthFactory
from infinigen.assets.utils.draw import leaf
from infinigen.core.tagging import tag_object
from infinigen.core.util.math import FixedSeed
from infinigen.core.util.random import log_uniform


class TussockMonocotFactory(MonocotGrowthFactory):
    def __init__(self, factory_seed, coarse=False):
        super(TussockMonocotFactory, self).__init__(factory_seed, coarse)
        with FixedSeed(factory_seed):
            self.stem_offset = uniform(0.0, 0.2)
            self.angle = uniform(np.pi / 20, np.pi / 18)
            self.z_drag = uniform(0.1, 0.2)
            self.min_y_angle = uniform(np.pi * 0.2, np.pi * 0.25)
            self.max_y_angle = np.pi / 2
            self.count = int(log_uniform(512, 1024))
            self.scale_curve = [(0, uniform(0.6, 1.0)), (1, uniform(0.6, 1.0))]

    @staticmethod
    def build_base_hue():
        if uniform(0, 1) < 0.5:
            return uniform(0.1, 0.15)
        else:
            return uniform(0.25, 0.35)

    def build_leaf(self, face_size):
        x_anchors = np.array([0, uniform(0.3, 0.7), 1.0])
        y_anchors = np.array([0, 0.01, 0])
        obj = leaf(x_anchors, y_anchors, face_size=face_size)
        self.decorate_leaf(obj)
        tag_object(obj, "tussock")
        return obj
