import subprocess

def start_landmark_search(path_sourcedata, landmarks_config, path_landmarks):
    #Todo: save the landmarks in the correct path_landmarks

    command = f"python Deep-MVLM/predict.py --c {landmarks_config} --n {path_sourcedata}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        # Handle the error here
        print(f"Error: {e}")
    finally:
        pass#subprocess.run("pkill -f unix_socket_name", shell=True)

    return True