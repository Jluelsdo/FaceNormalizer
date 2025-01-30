import subprocess
import os
import signal
import time
import torch
import psutil
def start_landmark_search(path_file, landmarks_config, path_landmarks, file_type=".stl"):
    #Todo: Integrate the landmarks search through the Deep-MVLM library
    torch.cuda.empty_cache()
    landmarks_name = path_file.split("/")[-1].replace(file_type, "_landmarks.txt")

    path_sourcedata = os.path.dirname(path_file)
    command = f"python Deep-MVLM/predict.py --c {landmarks_config} --n {path_file}"
    process = subprocess.Popen(command, shell=True)
    pid = process.pid
    path_file_landmarks = path_sourcedata + "/" + landmarks_name
    while(not os.path.exists(path_file_landmarks)):
        time.sleep(1)
    os.rename(path_file_landmarks, path_landmarks+"/"+landmarks_name)
    os.kill(pid, signal.SIGTERM)
    for proc in psutil.process_iter():
        try:
            cmd_line = proc.cmdline()
            if 'Deep-MVLM/predict.py' in cmd_line:
                proc.kill()
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    for root, dirs, files in os.walk(path_sourcedata):
        for file in files:
            if file.endswith(".vtk"):
                file_path = os.path.join(root, file)
                os.remove(file_path)
    return True
