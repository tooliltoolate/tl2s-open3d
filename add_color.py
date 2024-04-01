import numpy as np
import open3d as o3d


def add_color(pcd, color):
    print(pcd.point.positions.shape[0])
    pcd.point.colors = o3d.core.Tensor(
        np.tile(color, (pcd.point.positions.shape[0], 1)), dtype=o3d.core.Dtype.Float32)
    return pcd
