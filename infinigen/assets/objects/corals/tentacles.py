# Copyright (C) 2023, Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Lingjie Mei


import numpy as np
from numpy.random import uniform

import infinigen.core.util.blender as butil
from infinigen.assets.objects.trees.tree import build_radius_tree
from infinigen.assets.utils.misc import assign_material, sample_direction
from infinigen.assets.utils.nodegroup import geo_radius
from infinigen.core import surface
from infinigen.core.nodes.node_wrangler import Nodes, NodeWrangler
from infinigen.core.placement.factory import make_asset_collection
from infinigen.core.tagging import COMBINED_ATTR_NAME
from infinigen.core.util.blender import deep_clone_obj
from infinigen.core.util.color import hsv2rgba


def build_tentacles(**kwargs):
    n_branch = 5
    n_major = 8
    branch_config = {
        "n": n_branch,
        "path_kargs": lambda idx: {
            "n_pts": n_major,
            "std": 0.5,
            "momentum": 0.5,
            "sz": 0.008,
        },
        "spawn_kargs": lambda idx: {"init_vec": sample_direction(0.6)},
    }

    obj = build_radius_tree(None, branch_config, uniform(0.002, 0.004))
    surface.add_geomod(obj, geo_radius, apply=True, input_args=["radius"])
    return obj


def make_min_distance_points_fn(min_distance):
    def points_fn(nw: NodeWrangler, points):
        return nw.new_node(
            Nodes.MergeByDistance,
            input_kwargs={"Geometry": points, "Distance": min_distance},
        )

    return points_fn


def make_radius_points_fn(min_distance, radius_threshold):
    def points_fn(nw: NodeWrangler, points):
        radius = nw.vector_math("DISTANCE", nw.new_node(Nodes.InputPosition), [0] * 3)
        points = nw.new_node(
            Nodes.MergeByDistance,
            input_kwargs={
                "Geometry": points,
                "Selection": nw.compare("LESS_THAN", radius, radius_threshold * 1.5),
                "Distance": min_distance * 2,
            },
        )
        points = nw.new_node(
            Nodes.MergeByDistance,
            input_kwargs={"Geometry": points, "Distance": min_distance},
        )
        points = nw.new_node(
            Nodes.SeparateGeometry,
            [points, nw.compare("GREATER_THAN", radius, radius_threshold)],
        )
        return points

    return points_fn


def make_upward_points_fn(min_distance, max_angle):
    def points_fn(nw: NodeWrangler, points, normal):
        points = nw.new_node(
            Nodes.SeparateGeometry,
            [points, nw.compare_direction("LESS_THAN", normal, [0, 0, 1], max_angle)],
        )
        return nw.new_node(
            Nodes.MergeByDistance,
            input_kwargs={"Geometry": points, "Distance": min_distance},
        )

    return points_fn


def geo_tentacles(
    nw: NodeWrangler, tentacles, points_fn=None, density=500, realize=True
):
    geometry = nw.new_node(
        Nodes.GroupInput, expose_input=[("NodeSocketGeometry", "Geometry", None)]
    )
    tentacles = nw.new_node(Nodes.CollectionInfo, [tentacles, True, True])

    points, normal, rotation = nw.new_node(
        Nodes.DistributePointsOnFaces,
        input_kwargs={"Mesh": geometry, "Density": density},
    ).outputs
    rotation = nw.new_node(
        Nodes.RotateEuler,
        input_kwargs={"Rotation": rotation, "Angle": nw.uniform(0, 2 * np.pi)},
        attrs={"rotation_type": "AXIS_ANGLE", "space": "LOCAL"},
    )

    points = surface.eval_argument(nw, points_fn, points=points, normal=normal)
    tentacles = nw.new_node(
        Nodes.InstanceOnPoints,
        input_kwargs={
            "Points": points,
            "Instance": tentacles,
            "Pick Instance": True,
            "Rotation": rotation,
            "Scale": nw.uniform([0.6] * 3, [1.0] * 3, data_type="FLOAT_VECTOR"),
        },
    )
    if realize:
        realize_instances = nw.new_node(
            Nodes.RealizeInstances, input_kwargs={"Geometry": tentacles}
        )
    else:
        realize_instances = tentacles

    group_output = nw.new_node(
        Nodes.GroupOutput, input_kwargs={"Geometry": realize_instances}
    )


def shader_tentacles(nw: NodeWrangler, base_hue=0.3):
    roughness = 0.8
    specular = 0.25
    color = hsv2rgba((base_hue + uniform(-0.1, 0.1)) % 1, uniform(0.4, 0.6), 0.5)
    principled_bsdf = nw.new_node(
        Nodes.PrincipledBSDF,
        input_kwargs={
            "Base Color": color,
            "Roughness": roughness,
            "Specular IOR Level": specular,
            "Subsurface Weight": 0.01,
        },
    )
    fresnel_color = hsv2rgba(uniform(0, 1), 0.6, 0.6)
    fresnel_bdsf = nw.new_node(Nodes.PrincipledBSDF, [fresnel_color])
    mixed_shader = nw.new_node(
        Nodes.MixShader, [nw.new_node(Nodes.Fresnel), principled_bsdf, fresnel_bdsf]
    )
    return mixed_shader


def apply(obj, points_fn, density, realize=True, base_hue=0.3):
    tentacles = deep_clone_obj(obj)
    if COMBINED_ATTR_NAME in tentacles.data.attributes:
        tentacles.data.attributes.remove(tentacles.data.attributes[COMBINED_ATTR_NAME])

    instances = make_asset_collection(build_tentacles, 5, "spikes", verbose=False)
    surface.add_geomod(
        tentacles,
        geo_tentacles,
        apply=realize,
        input_args=[instances, points_fn, density, realize],
    )

    butil.delete_collection(instances)
    assign_material(
        tentacles, surface.shaderfunc_to_material(shader_tentacles, base_hue)
    )
    return tentacles
