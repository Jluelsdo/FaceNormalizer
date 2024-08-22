import numpy as np
from scipy.spatial import ConvexHull, Delaunay
import trimesh
import os
class Cutting:

    def run_cutting(self, path_sourcedata, path_target_cutting, order_cutting, path_target_landmarks, save_intermediate_step=True):

        for file in os.listdir(path_sourcedata):
            if not file.endswith(".stl"):
                continue

            file_path = os.path.join(path_sourcedata, file)
            path_landmarks = os.path.join(path_target_landmarks, file.replace(".stl", "_landmarks.txt"))
            if not os.path.exists(path_landmarks):
                print(f"Error: Landmarks file does not exist at {path_landmarks}!")
                continue
            landmarks = np.loadtxt(path_landmarks)
            mesh = trimesh.load_mesh(file_path)

            # Cut the face
            for cut in order_cutting:
                if cut == "outline":
                    self._cutting_outlines_through_hull(file_path, os.path.join(path_target_cutting, file), path_landmarks, save_intermediate_step)
                elif cut == "upper_face":
                    try:
                        cut_vertices_upper = self._cut_upper_face(landmarks, cut_vertices_lower)
                        cut_mesh = self._simulate_faces(cut_vertices_upper)
                    except NameError:
                        cut_vertices_upper = self._cut_upper_face(landmarks, mesh.vertices)
                elif cut == "lower_face":
                    try:
                        cut_vertices_lower = self._cut_lower_face(landmarks, cut_vertices_upper)
                        cut_mesh = self._simulate_faces(cut_vertices_lower)
                    except NameError:
                        cut_vertices_lower = self._cut_lower_face(landmarks, mesh.vertices)

            # Export the cut mesh
            if save_intermediate_step:
                cut_mesh.export(os.path.join(path_target_cutting, file.replace(".stl", "_cut.stl")))
            cut_mesh.export(file_path)
        return True

    def _simulate_faces(self, vertices):
        """Due to the cutting of the face we need to simulate the faces missing. This is done by triangulating the face."""
        mesh = trimesh.Trimesh(vertices=vertices)
        tri = Delaunay(mesh.vertices[:,:2])
        return trimesh.Trimesh(vertices=vertices, faces=tri.simplices)

    def _cutting_outlines_through_hull(self, path_sourcedata, path_targetdata, path_landmarks, save_intermediate_step):
        """Start the cutting of the face."""
        landmarks = np.loadtxt(path_landmarks)
        hull = ConvexHull(landmarks)
        inflated_points = np.zeros((0,3))
        center_hull = np.mean(hull.points, axis=0)

        for point in hull.points:
            inflated_point = center_hull + 1.5 *(point-center_hull)
            inflated_points = np.vstack((inflated_points, inflated_point))

        inflated_hull = ConvexHull(inflated_points)
        mesh = trimesh.load_mesh(path_sourcedata)

        verticices = mesh.vertices
        filtered_vertices = []
        for vertex in verticices:
            if inflated_hull.equations[0,0]*vertex[0] + inflated_hull.equations[0,1]*vertex[1] + inflated_hull.equations[0,2]*vertex[2] + inflated_hull.equations[0,3] <= 0:
                filtered_vertices.append(vertex)

        cut_mesh = self._simulate_faces(filtered_vertices)
        cut_mesh.export(path_sourcedata)

        if save_intermediate_step:
            cut_mesh.export(path_targetdata.replace(".stl", "_cut.stl"))
        return True 

    def _cut_upper_face(self, landmarks, vertices):
        # Cut upper face
        p1 = landmarks[32]
        p2 = landmarks[33]
        p3 = (landmarks[34] + landmarks[44]) / 2
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        normal /= np.linalg.norm(normal)
        d = -np.dot(normal, p1)
        # Cut the model with the plane using a vectorized operation
        condition = np.dot(vertices, normal) + d >= 0
        return vertices[condition]

    def _cut_lower_face(self, landmarks, vertices):
        p1 = landmarks[62]
        p2 = landmarks[67]
        p3 = landmarks[72]
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        normal /= np.linalg.norm(normal)
        d = -np.dot(normal, p1)

        # Cut the model with the plane using a vectorized operation
        condition = np.dot(vertices, normal) + d >= 0
        return vertices[condition]