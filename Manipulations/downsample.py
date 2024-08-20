import trimesh

def downsample(input_file, output_file, num_samples):
    """
    Load the mesh and downsample it to the number of samples set in the config.json file.
    simplify_quadratic_decimation is a wrapper for open3d.geometry.TriangleMesh
    """
    # Load the mesh using trimesh
    mesh = trimesh.load_mesh(input_file)
    
    # Simplify the mesh using trimesh's simplify_quadratic_decimation
    simplified_mesh = mesh.simplify_quadratic_decimation(num_samples)
    
    # Save the simplified mesh as an STL file
    simplified_mesh.export(output_file)
    return True
