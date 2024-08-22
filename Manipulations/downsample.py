import trimesh
import os

def downsample(input_path, output_path, num_samples, save_intermediate_step=True):
    """
    Load the mesh and downsample it to the number of samples set in the config.json file.
    simplify_quadratic_decimation is a wrapper for open3d.geometry.TriangleMesh
    """
    # Iterate through all files within input_path
    for file_name in os.listdir(input_path):
        # Construct the full file path
        file_path = os.path.join(input_path, file_name)
        
        # Check if the file is a mesh file
        if not file_name.endswith('.stl'):
            continue
        # Load the mesh using trimesh
        mesh = trimesh.load_mesh(file_path)
        
        # Simplify the mesh using trimesh's simplify_quadratic_decimation
        simplified_mesh = mesh.simplify_quadratic_decimation(num_samples)
        
        # Save the simplified mesh as an STL file
        simplified_mesh.export(file_path)
        if save_intermediate_step:
            file_output_path = os.path.join(output_path, file_name)
            simplified_mesh.export(file_output_path.replace(".stl", "_simplified.stl"))
    return True
