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

            self.path_execution_doc = config["DataSource"]["path_execution_doc"]
            self.path_log = config["DataSource"]["path_log"]
            self.version = config["DataSource"]["version"]


    def run_normalization(self):
        """Run the normalization of the face. Logic is described within the Readme.md ManipulationOrder."""
        if not self._check_order_of_manipulation():
            return False
        print(f"Order of manipulation: {self.order_of_manipulation}")
        file_list = self._get_file_list()

        if not os.path.exists(self.path_execution_doc):
            self._create_csv_documentation(file_list)


        total_files = len(file_list)
        processed_files = 0
        for file_name in file_list:
            processed_files += 1
            percentage = (processed_files / total_files) * 100
            print(f"Processing {file_name} ({percentage:.2f}%)")

            for manipulation in self.order_of_manipulation:
                if manipulation == "Landmarks":
                    self._run_landmarks(file_name)
                elif manipulation == "Determine number of vertices":
                    self._run_determine_number_of_vertices()
                elif manipulation == "Determine orientation":
                    self._run_determine_orientation()
                elif manipulation == "Rescale size":
                    self._run_rescale()
                elif manipulation == "Cutting":
                    self._run_cutting(file_name)
                elif manipulation == "Rotate face":
                    self._run_rotate()
                elif manipulation == "Translate face":
                    self._run_translate()
                elif manipulation == "Normalize number of vertices":
                    self._run_normalize_number_of_vertices(file_name)
                self._update_csv_status(file_name, "Done")

    def _update_csv_status(self, filename, new_status):
        """
        Updates the status of a specific row in a CSV file without rewriting the whole file.
        """
        with open(self.path_execution_doc, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile,  delimiter=";")
            rows = list(reader)

        for row in rows:
            if row['File'] == filename.split('/')[-1]:
                row["Status"] = new_status
                break

        with open(self.path_execution_doc, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(rows)

    def _create_csv_documentation(self, file_list):
        """Create a csv file to document the manipulations."""
        with open(self.path_log, 'w') as log_file:
            log_file.write("General Information\n")
            log_file.write(f"Version: {self.version}\n")
            log_file.write(f"Path Source Data: {self.path_sourcedata}\n")
            log_file.write(f"Path Target Landmarks: {self.path_target_landmarks}\n")
            log_file.write(f"Path Target Cutting: {self.path_target_cutting}\n")
            log_file.write(f"Path Target Normalize Number of Vertices: {self.path_target_normalize_number_of_vertices}\n")
            log_file.write(f"Number of Vertices: {self.normalize_number_of_vertices}\n")
            log_file.write(f"Landmarks Config: {self.landmarks_config}\n")
            log_file.write(f"Cutting Config: {self.cutting_config}\n")

        with open(self.path_execution_doc, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(["File", "Status"])
            for file in file_list:
                csv_writer.writerow([file.split('/')[-1], ""])

    def _get_csv_reader(self):
        """Get the csv reader."""
        csv_file = open(self.path_execution_doc, 'r')
        csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')
        next(csv_reader)
        return csv_reader

    def _get_file_list(self):
        """Get the list of files to be processed."""
        file_list = []
        if os.path.exists(self.path_execution_doc):
            csv_reader = self._get_csv_reader()
            for row in csv_reader:
                if row[1] != 'Done':
                    file_list.append(os.path.join(self.path_sourcedata, row[0]))
            return file_list

        for root, dirs, files in os.walk(self.path_sourcedata):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    file_list.append(file_path)
        return file_list

    def _check_order_of_manipulation(self):
        """Check if the order of manipulation is correct."""
        landmark_index = self.order_of_manipulation.index("Landmarks") if "Landmarks" in self.order_of_manipulation else 1000
        cutting_index = self.order_of_manipulation.index("Cutting") if "Cutting" in self.order_of_manipulation else 1000
        rotate_index = self.order_of_manipulation.index("Rotate face") if "Rotate face" in self.order_of_manipulation else 1000
        translate_index = self.order_of_manipulation.index("Translate face") if "Translate face" in self.order_of_manipulation else 1000
        centering_index = self.order_of_manipulation.index("Centering") if "Centering" in self.order_of_manipulation else 1000
        rescale_index = self.order_of_manipulation.index("Rescale size") if "Rescale size" in self.order_of_manipulation else 1000
        normalize_number_of_vertices_index = self.order_of_manipulation.index("Normalize number of vertices") if "Normalize number of vertices" in self.order_of_manipulation else -1
        add_noise_index = self.order_of_manipulation.index("Add noise") if "Add noise" in self.order_of_manipulation else 1000


        if landmark_index > cutting_index or landmark_index > rotate_index or landmark_index > translate_index:
            print("Landmarks should be before Cutting, Rotate face and Translate face")
            return False
        if centering_index > rescale_index:
            print("Centering should be before Rescaling")
            return False
        if add_noise_index != len(self.order_of_manipulation)-1 and add_noise_index != 1000:
            print("Add Noise should be the last manipulation")
            return False

        # After manipulation order is checked, insert Landmarks when they have to be run again.
        if "Normalize number of vertices" in self.order_of_manipulation and "Normalize number of vertices" != self.order_of_manipulation[-1]:
            self.order_of_manipulation.insert(self.order_of_manipulation.index("Normalize number of vertices")+1, "Landmarks")
        if "Translate face" in self.order_of_manipulation:
            self.order_of_manipulation.insert(self.order_of_manipulation.index("Translate face")+1, "Landmarks")
        if "Rotate face" in self.order_of_manipulation:
            self.order_of_manipulation.insert(self.order_of_manipulation.index("Rotate face")+1, "Landmarks")
        if "Rescale size" in self.order_of_manipulation:
            self.order_of_manipulation.insert(self.order_of_manipulation.index("Rescale size")+1, "Landmarks")
        return True

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
