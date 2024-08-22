import subprocess
import os
import signal
import time

def start_landmark_search(path_sourcedata, landmarks_config, path_landmarks):
    """Start the landmark search for the face."""
    #Todo: Integrate the landmarks search through the Deep-MVLM library
    file_list = []
    for root, dirs, files in os.walk(path_sourcedata):
        for file in files:
            if file.endswith(".stl"):
                file_list.append(os.path.join(root, file))
    for file_path in file_list:
        command = f"python Deep-MVLM/predict.py --c {landmarks_config} --n {file_path}"
        process = subprocess.Popen(command, shell=True)
        pid = process.pid
        landmarks_name = file_path.split("/")[-1].replace(".stl", "_landmarks.txt")
        path_file_landmarks = path_sourcedata + "/" + landmarks_name
        while(not os.path.exists(path_file_landmarks)):
            time.sleep(1)
        os.rename(path_file_landmarks, path_landmarks+"/"+landmarks_name)
        os.kill(pid, signal.SIGTERM)


    # Remove files ending with .vtk from path_sourcedata
    for root, dirs, files in os.walk(path_sourcedata):
        for file in files:
            if file.endswith(".vtk"):
                file_path = os.path.join(root, file)
                os.remove(file_path)
    return True