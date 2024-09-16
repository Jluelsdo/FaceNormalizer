import json
from Manipulations.landmarks import start_landmark_search
from Manipulations.verticeNumber import NormalizeNumberOfVertices
from Manipulations.cut import Cutting
import os
import csv
class FaceNormalizer():

    def __init__(self):
        """Read settings made in the config.json file."""
        with open('config.json') as f:
            config = json.load(f)
        self.order_of_manipulation = config["ManipulationOrder"]
        self.normalize_number_of_vertices = config["Normalize number of vertices"]
        self.landmarks_config = config["Landmarks"]["LandmarksConfig"]
        self.cutting_config = config["Cutting"]

        if config["DataSource"]["type"] == "test":
            self.path_sourcedata = "Data/Testdata/original/testscan.stl"
            self.path_target_landmarks = "Data/Testdata/original"
            self.path_target_cutting = "Data/Testdata/original"+"/testscan_cut.stl"
            self.path_target_normalize_number_of_vertices = "Data/Testdata/original/testscan_normalized.stl"

        elif config["DataSource"]["type"] == "local":
            self.path_sourcedata = config["DataSource"]["path_source"]
            self.path_target_landmarks = config["DataSource"]["path_target_landmarks"]
            self.path_target_cutting = config["DataSource"]["path_target_cutting"]
            self.path_target_normalize_number_of_vertices = config["DataSource"]["path_target_normalize_number_of_vertices"]

            self.path_execution_list = config["DataSource"]["path_execution_list"]
            self.path_log = config["DataSource"]["path_log"]


    def run_normalization(self):
        """Run the normalization of the face. Logic is described within the Readme.md ManipulationOrder."""
        print(f"Order of manipulation: {self.order_of_manipulation}")
        file_list = []
        for root, dirs, files in os.walk(self.path_sourcedata):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    file_list.append(file_path)
        total_files = len(file_list)
        processed_files = 0
        for file_name in file_list:
            processed_files += 1
            percentage = (processed_files / total_files) * 100
            print(f"Processing {file_name} ({percentage:.2f}%)")
            # Rule 1 Run all Manipulations which are not dependent on other manipulations
            landmarks_detected = False
            if "Landmarks" in self.order_of_manipulation:
                self._run_landmarks(file_name)
                landmarks_detected = True
            if "Determine number of vertices" in self.order_of_manipulation:
                self._run_determine_number_of_vertices()
            if "Determine orientation" in self.order_of_manipulation and landmarks_detected:
                self._run_determine_orientation()
            else:
                print("Determine orientation is dependent on landmarks. Please add Landmarks to config.json.")

            for manipulation in self.order_of_manipulation:
                if manipulation == "Rescale size":
                    self._run_rescale()
                elif manipulation == "Cutting":
                    self._run_cutting(file_name)
                elif manipulation == "Rotate face":
                    self._run_rotate()
                elif manipulation == "Translate face":
                    self._run_translate()
                    self._run_landmarks(file_name)
                elif manipulation == "Normalize number of vertices":
                    self._run_normalize_number_of_vertices()
                    self._run_landmarks(file_name)

    

    def _run_landmarks(self, path_file):
        """Run the normalization of the face using landmarks."""
        start_landmark_search(path_file, self.landmarks_config, self.path_target_landmarks)
        print("Landmarks done")
        return True

    def _run_rescale(self):
        """Run the normalization of the face using rescaling."""
        print("Rescale")

    def _run_cutting(self, path_file):
        """Run the normalization of the face using cutting."""
        cutting = Cutting()
        cutting.run_cutting(path_file, self.path_target_cutting, self.cutting_config["OrderCutting"], self.path_target_landmarks, self.cutting_config["FaceInflation"], self.cutting_config["SaveIntermediateSteps"])
        print("Cutting done")
        return True

    def _run_rotate(self):
        """Run the normalization of the face using rotation."""
        print("Rotate")

    def _run_translate(self):
        """Run the normalization of the face using translation."""
        print("Translate")

    def _run_normalize_number_of_vertices(self, path_file):
        """Run the normalization of the face using the normalization of the number of vertices."""
        normalizeNumberOfVertices = NormalizeNumberOfVertices()
        normalizeNumberOfVertices.normalize(path_file, self.path_target_normalize_number_of_vertices, self.normalize_number_of_vertices["Number of Vertices"], self.normalize_number_of_vertices["SaveIntermediateSteps"])
        print("Normalize number of vertices")

    def _run_determine_number_of_vertices(self):
        """Run the normalization of the face using the determination of the number of vertices."""
        print("Determine number of vertices")

    def _run_determine_orientation(self):
        """Run the normalization of the face using the determination of the orientation."""
        print("Determine orientation")

if __name__ == '__main__':
    faceNormalizer = FaceNormalizer()
    faceNormalizer.run_normalization()
