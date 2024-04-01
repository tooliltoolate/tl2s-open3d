import load_from_ply as load
import open3d as o3d
import open3d.core as o3c
import add_color as color
# import numpy as np

a = load.load_from_ply('test_ply_2.ply')
pcd = o3d.t.geometry.PointCloud(o3c.Tensor(a, o3c.float32))
pcd = color.add_color(pcd, [0, 0, 0])
o3d.visualization.draw_geometries([pcd.to_legacy()])
