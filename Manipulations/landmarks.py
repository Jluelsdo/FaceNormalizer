import subprocess
import os
import signal
import time

def start_landmark_search(path_sourcedata, landmarks_config, path_landmarks):
    #Todo: save the landmarks in the correct path_landmarks
    #Todo: Integrate the landmarks search through the Deep-MVLM library
    #Todo: Add the search for outside testing (Mulitple Landmarks n paths)

    command = f"python Deep-MVLM/predict.py --c {landmarks_config} --n {path_sourcedata}"
    process = subprocess.Popen(command, shell=True)
    pid = process.pid
    while(not os.path.exists("Data/Testdata/original/testscan_landmarks.txt")):
        time.sleep(1)
    os.kill(pid, signal.SIGTERM)
    return True