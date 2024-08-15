import subprocess

def start_landmark_search(path_sourcedata, landmarks_config, path_landmarks):
    #Todo: save the landmarks in the correct path_landmarks

    command = f"python predict.py --c {landmarks_config} --n {path_sourcedata}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd="Deep-MVLM")
    process.wait()

    return True