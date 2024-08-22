import numpy as np
from scipy.spatial import ConvexHull, Delaunay
import trimesh
class Cutting:

    def _simulate_faces(self, vertices):
        """Due to the cutting of the face we need to simulate the faces missing. This is done by triangulating the face."""
        mesh = trimesh.Trimesh(vertices=vertices)
        tri = Delaunay(mesh.vertices[:,:2])
        return trimesh.Trimesh(vertices=vertices, faces=tri.simplices)

    def cutting_outlines_through_hull(self, path_sourcedata, path_targetdata, path_landmarks, cutting_config):
        """Start the cutting of the face."""
        print("Cutting")
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

        cut_mesh.export(path_targetdata)
        return True 

    def cut_upper_lower_face(self, path_sourcedata, path_targetdata, path_landmarks, cutting_config):
        landmarks = np.loadtxt(path_landmarks)
        mesh = trimesh.load_mesh(path_sourcedata)
        cut_vertices_upper = self._cut_upper_face(landmarks, mesh)
        cut_vertices_lower = self._cut_lower_face(landmarks, cut_vertices_upper)
        cut_mesh = self._simulate_faces(cut_vertices_lower)
        cut_mesh.export(path_targetdata)
        return True

    def _cut_upper_face(self, landmarks, mesh):
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
        condition = np.dot(mesh.vertices, normal) + d >= 0
        return mesh.vertices[condition]

    def _cut_lower_face(self, landmarks, cut_vertices_upper):
        p1 = landmarks[62]
        p2 = landmarks[67]
        p3 = landmarks[72]
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        normal /= np.linalg.norm(normal)
        d = -np.dot(normal, p1)

        # Cut the model with the plane using a vectorized operation
        condition = np.dot(cut_vertices_upper, normal) + d >= 0
        return cut_vertices_upper[condition]

cutting = Cutting()
cutting.cut_upper_lower_face("Data/Testdata/original/testscan.stl", "Data/Testdata/original/testscan_cut.stl", "Data/Testdata/original/testscan_landmarks.txt", None)