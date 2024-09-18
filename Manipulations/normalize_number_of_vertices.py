import trimesh
import os
import math

def normalize_number_of_vertices(input_path, output_path, num_samples, save_intermediate_step=True):
    """
    Load the mesh and decide if there are more or less verticies than number of vertices.
    If there are more downsample it to the number of samples given, oterwise upsample it.
    simplify_quadratic_decimation is a wrapper for open3d.geometry.TriangleMesh
    """
    # Iterate through all files within input_path
    for file_name in os.listdir(input_path):
        file_path = os.path.join(input_path, file_name)
        if not file_name.endswith('.stl'):
            continue
        mesh = trimesh.load_mesh(file_path)
        while num_samples != mesh.vertices.shape[0]:
            # Downsample the mesh if it has more vertices than num_samples
            if mesh.vertices.shape[0] > num_samples:
                mesh = downsample(mesh, num_samples)
            elif mesh.vertices.shape[0] < num_samples:
                mesh = upsample(mesh, num_samples)
        # Save the simplified mesh as an STL file
        mesh.export(file_path)
        if save_intermediate_step:
            file_output_path = os.path.join(output_path, file_name)
            mesh.export(file_output_path.replace(".stl", "_simplified.stl"))
    return True


def downsample(mesh, num_samples):
    normalized_mesh = mesh.simplify_quadratic_decimation(num_samples)
    return normalized_mesh

def upsample(mesh, num_samples):
    subdivision_level = 1
    tolerance = 0.1
    while mesh.vertices.shape[0] < num_samples:
        mesh = mesh.subdivide(level=subdivision_level)
        # Check if within tolerance
        if abs(mesh.vertices.shape[0] - num_samples) / num_samples <= tolerance:
            break
        # Adjust subdivision level
        if mesh.vertices.shape[0] > num_samples:
            subdivision_level -= 1
        else:
            subdivision_level += 1
    return mesh
