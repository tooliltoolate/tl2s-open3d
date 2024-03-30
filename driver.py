import load_from_ply as load
import open3d as o3d


a = load.load_from_ply('test_ply_2.ply')
#a = o3d.io.read_point_cloud('test_ply_2.ply')
o3d.visualization.draw_geometries([a])