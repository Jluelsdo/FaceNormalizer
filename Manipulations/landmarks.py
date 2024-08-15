import subprocess

def start_landmark_search(path_sourcedata, landmarks_config, path_landmarks):
    #Todo: save the landmarks in the correct path_landmarks

    command = f"python Deep-MVLM/predict.py --config {landmarks_config} --name {path_sourcedata}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()

    return True