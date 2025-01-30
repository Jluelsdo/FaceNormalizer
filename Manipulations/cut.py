import numpy as np
from scipy.spatial import ConvexHull, Delaunay
import trimesh
import os
class Cutting:

    def run_cutting(self, file_path, path_target_cutting, order_cutting, path_target_landmarks, face_inflation=2, save_intermediate_step=True, file_type=".stl"):
        file_name = file_path.split("/")[-1]

        path_landmarks = os.path.join(path_target_landmarks, file_name.replace(file_type, "_landmarks.txt"))
        if not os.path.exists(path_landmarks):
            print(f"Error: Landmarks file does not exist at {path_landmarks}!")
        landmarks = np.loadtxt(path_landmarks)
        cut_mesh = trimesh.load_mesh(file_path)
        print(f"Face inflation{face_inflation}")
        for cut in order_cutting:
            if cut == "outline":
                cut_mesh = self._cutting_outlines_through_hull(landmarks,cut_mesh, face_inflation=2.0, save_intermediate_step=save_intermediate_step)
            elif cut == "mouth":
                cut_mesh = self._cut_out_mouth(landmarks,cut_mesh,face_inflation=2.0)
            elif cut == "upper_face":
                try:
                    cut_vertices = self._cut_upper_face(landmarks, cut_vertices)
                    cut_mesh = self._simulate_faces(cut_vertices)
                except NameError:
                    mesh = trimesh.load_mesh(file_path)
                    cut_vertices = self._cut_upper_face(landmarks, mesh.vertices)
            elif cut == "lower_face":
                try:
                    cut_vertices = self._cut_lower_face(landmarks, cut_vertices)
                    cut_mesh = self._simulate_faces(cut_vertices)
                except NameError:
                    mesh = trimesh.load_mesh(file_path)
                    cut_vertices = self._cut_lower_face(landmarks, mesh.vertices)
            """elif cut == "back_face":
                try:
                    cut_vertices = self._cut_back_face(landmarks, cut_vertices)
                    cut_mesh = self._simulate_faces(cut_vertices)
                except NameError:
                    mesh = trimesh.load_mesh(file_path)
                    cut_vertices = self._cut_back_face(landmarks, mesh.vertices)
            """

        # Export the cut mesh
        if save_intermediate_step:
            cut_mesh.export(os.path.join(path_target_cutting, file_name.replace(file_type, "_cut"+file_type)))
        cut_mesh.export(file_path)
        return True

    def _simulate_faces(self, vertices):
        """Due to the cutting of the face we need to simulate the faces missing. This is done by triangulating the face."""
        mesh = trimesh.Trimesh(vertices=vertices)
        tri = Delaunay(mesh.vertices[:,:2])
        return trimesh.Trimesh(vertices=vertices, faces=tri.simplices)

    def _cutting_outlines_through_hull(self, landmarks, mesh, face_inflation=2, save_intermediate_step=True):
        """Start the cutting of the face."""
        hull = ConvexHull(landmarks)
        inflated_points = np.zeros((0,3))
        center_hull = np.mean(hull.points, axis=0)

        for point in hull.points:
            inflated_point = center_hull + face_inflation *(point-center_hull)
            inflated_points = np.vstack((inflated_points, inflated_point))

        inflated_hull = ConvexHull(inflated_points)

        verticices = mesh.vertices
        filtered_vertices = []
        for vertex in verticices:
            if inflated_hull.equations[0,0]*vertex[0] + inflated_hull.equations[0,1]*vertex[1] + inflated_hull.equations[0,2]*vertex[2] + inflated_hull.equations[0,3] <= 0:
                filtered_vertices.append(vertex)

        cut_mesh = self._simulate_faces(filtered_vertices)

        return cut_mesh 

    def _cut_out_mouth(self, landmarks, mesh, face_inflation=2):
        #Choose landmarks surrounding the mouth
        selected_landmarks = landmarks[46:55]

        # Create hull around the mouth and inflate it
        hull = ConvexHull(selected_landmarks)
        inflated_points = np.zeros((0,3))
        center_hull = np.mean(hull.points, axis=0)

        for point in hull.points:
            inflated_point = center_hull + face_inflation *(point-center_hull)
            inflated_points = np.vstack((inflated_points, inflated_point))

        inflated_hull = ConvexHull(inflated_points)

        verticices = mesh.vertices

        # Decide if the vertex is inside the inflated hull only keep the once outside
        filtered_vertices = []
        for vertex in verticices:
            if not np.all(np.dot(inflated_hull.equations[:, :-1], vertex) + inflated_hull.equations[:, -1] <= 0):
                filtered_vertices.append(vertex)

        cut_mesh = self._simulate_faces(filtered_vertices)

        return cut_mesh

    def _cut_upper_face(self, landmarks, vertices):
        p1 = landmarks[41]
        p2 = landmarks[37]
        p3 = landmarks[39]

        # Calculate the normal of the plane
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        normal /= np.linalg.norm(normal)
        d = -np.dot(normal, p1)

        # Move the plane to the point 
        p4 = (landmarks[44]+landmarks[34])/2
        d = -np.dot(normal, p4)

        # Cut the model with the plane using a vectorized operation
        point_position = np.dot(landmarks[49], normal) + d
        if point_position >= 0:
            condition = np.dot(vertices, normal) + d >= 0
        else:
            condition = np.dot(vertices, normal) + d <= 0
        return vertices[condition]

    

    def _cut_lower_face(self, landmarks, vertices):
        p1 = landmarks[41]
        p2 = landmarks[37]
        p3 = landmarks[39]

        # Calculate the normal of the plane
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        normal /= np.linalg.norm(normal)
        d = -np.dot(normal, p1)

        # Move the plane down to the point 67
        p67 = landmarks[67]
        d = -np.dot(normal, p67)

        # Cut the model with the plane using a vectorized operation
        point_position = np.dot(landmarks[45], normal) + d
        if point_position >= 0:
            condition = np.dot(vertices, normal) + d >= 0
        else:
            condition = np.dot(vertices, normal) + d <= 0
        return vertices[condition]
    
    def _cut_back_face(self, landmarks, vertices):
        # Find the three landmarks with the smallest y coordinate (furthest back)
        back_landmarks = landmarks[np.argsort(landmarks[:, 1])[:3]]
        # Define the plane using these three points
        p1, p2, p3 = back_landmarks
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        normal /= np.linalg.norm(normal)
        d = -np.dot(normal, p1)
        # Make the plane parallel to the y-axis by setting the y component of the normal to 0
        normal[1] = 0
        normal /= np.linalg.norm(normal)
        # Cut the model with the plane using a vectorized operation
        # Check if the point landmark[45] is in front or behind the plane
        point_position = np.dot(landmarks[45], normal) + d
        if point_position >= 0:
            condition = np.dot(vertices, normal) + d >= 0
        else:
            condition = np.dot(vertices, normal) + d <= 0
        return vertices[condition]