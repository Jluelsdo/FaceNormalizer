import json
from Manipulations.landmarks import start_landmark_search
class FaceNormalizer():

    def __init__(self):
        """Read settings made in the config.json file."""
        with open('config.json') as f:
            config = json.load(f)
        self.order_of_manipulation = config["ManipulationOrder"]
        self.normalize_number_of_vertices = config["Normalize number of vertices"]
        self.landmarks_config = config["Landmarks"]["LandmarksConfig"]

        if config["DataSource"] == "test":
            self.path_sourcedata = "../Data/Testdata/original/testscan.stl"
            self.path_targetdata = "../Data/Testdata/target"


    def run_normalization(self):
        """Run the normalization of the face."""
        print(f"Order of manipulation: {self.order_of_manipulation}")
        for manipulation in self.order_of_manipulation:
            if manipulation == "Landmarks":
                self._run_landmarks()
            elif manipulation == "Rescale size":
                self._run_rescale()
            elif manipulation == "Cut face":
                self._run_cutting()
            elif manipulation == "Rotate face":
                self._run_rotate()
            elif manipulation == "Translate face":
                self._run_translate()
            elif manipulation == "Normalize number of vertices":
                self._run_normalize_number_of_vertices()

    def _run_landmarks(self):
        """Run the normalization of the face using landmarks."""
        start_landmark_search(self.path_sourcedata, self.landmarks_config, self.path_targetdata)
        print("Landmarks done")
        return True

    def _run_rescale(self):
        """Run the normalization of the face using rescaling."""
        print("Rescale")

    def _run_cutting(self):
        """Run the normalization of the face using cutting."""
        print("Cutting")
    
    def _run_rotate(self):
        """Run the normalization of the face using rotation."""
        print("Rotate")

    def _run_translate(self):
        """Run the normalization of the face using translation."""
        print("Translate")

    def _run_normalize_number_of_vertices(self):
        """Run the normalization of the face using the normalization of the number of vertices."""
        print("Normalize number of vertices")



if __name__ == '__main__':
    faceNormalizer = FaceNormalizer()
    faceNormalizer.run_normalization()
