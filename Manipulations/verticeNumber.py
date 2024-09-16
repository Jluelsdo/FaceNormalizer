import os
import trimesh
import numpy as np
from scipy.spatial import Delaunay

class NormalizeNumberOfVertices:
    def __init__(self):
        pass

    def _search_files(self, input_path):
        """
        Search for mesh files in the input path.
        """
        mesh_files = []
        for file_name in os.listdir(input_path):
            file_path = os.path.join(input_path, file_name)
            if file_name.endswith('.stl'):
                mesh_files.append(file_path)
        return mesh_files

    def _sample_points_uniformly_on_surface(self, mesh, num_samples):
        points, _ = trimesh.sample.sample_surface_even(mesh, num_samples)
        return points
    
    def _points_to_mesh(self, points):
        vertices = points
        faces = np.empty((0, 3), dtype=int)  # No faces, just points
        return trimesh.Trimesh(vertices=vertices, faces=faces)

    def normalize(self, input_path, output_path, num_samples, save_intermediate_step=True):
        """
        Normalize the number of vertices in the mesh files.
        """
        mesh_files = self._search_files(input_path)
        for file_path in mesh_files:
            original_mesh = trimesh.load_mesh(file_path)
            vertices = self._sample_points_uniformly_on_surface(original_mesh, num_samples)
            tri = Delaunay(vertices[:, :2])
            faces = tri.simplices
            normalized_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
            normalized_mesh.export(file_path)
            if save_intermediate_step:
                file_output_path = os.path.join(output_path, os.path.basename(file_path))
                normalized_mesh.export(file_output_path)
