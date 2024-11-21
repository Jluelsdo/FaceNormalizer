Package to normalize a 3D human face, in orientation, location and number of verticies. It is used to normalize the face before feeding it to a neural network.

## Installation

To install the submodules after cloning run
``` git submodule update --init --recursive ```

The software is tested with Python 3.8.10, due to the submodule Deep-MVLM, other versions of Python might cause issues.
To install the requirements run
``` pip install -r requirements.txt ```

## Config.json
Within the config.json the user can specify the order of manipulation and the parameters for each manipulation.
The following is an example of a config.json file:

```json
{
    "DataSource":{
        "type":"local",
        "path_source":"../data/in_progress",
        "path_target_landmarks":"../data/landmarks",
        "path_target_cutting":"../data/cutting",
        "path_target_normalize_number_of_vertices":"../data/normalize_number_of_vertices"
    },
    "ManipulationOrder": [
        "Landmarks",
        "Cutting",
        "Rescale size",
        "Rotate face",
        "Translate face",
        "Add noise",
        "Normalize number of vertices"
    ],
    "Landmarks": {
        "LandmarksConfig": "Deep-MVLM/configs/DTU3D-geometry.json"
    },
    "Normalize number of vertices": {
        "Number of Vertices": 1000,
        "SaveIntermediateSteps": true
    },

    "Cutting": {
        "OrderCutting": ["mouth", "outline", "upper_face", "lower_face"],
        "SaveIntermediateSteps": true
    },
}
```

### DataSource
The DataSource defines the type of datasource and the location. Options for "type" are "test" and "local". If "type" is "test" the data will be used from the repo "Data/Testdata/original".
If "type" is "local" the data will be used from the location specified in "path_source". If the user wants to save intermediate steps they have to set "SaveIntermediateSteps" in the respective manipulation to True. Furthermore they must define the locations specified in "path_target_landmarks", "path_target_cutting" and "path_target_normalize_number_of_vertices" where the intermediate steps will be saved.

### ManipulationOrder
The order of the manipulations to be applied to the face. The manipulations are applied in the order they are specified in the list. If a manipulation is not specified in the list, it will not be applied. It is recommended to have "Landmarks" as the first manipulation, as the other manipulations depend on the landmarks or to have existing landmarks for the stl scans that are being processed within the "path_target_landmarks" folder.

The order of manipulations follows the following rules:
1. If it wont change the outcome of the result always apply the manipulation before every manipulation where this does not apply
2. If a manipulation A depends on another manipulation B don't allow to execute A before B
3. If a manipulation changes the location of vertices apply those changes to all landmarks
4. If manipulations can be set together in groups, add them to groups (Cutting)

The file normalize.py ensures that the manipulations are applied in the correct order.

![Data Preperation Pipeline](Documentation/data_preperation_pipeline.png)

### Manipulation Configurations
The user can specify the parameters for each manipulation. The parameters are specified in the respective manipulation. The user can also specify the location of the landmarks configuration file in the "Landmarks" manipulation. The user can also specify the number of vertices in the "Normalize number of vertices" manipulation. The user can also specify the order of cutting in the "Cutting" manipulation.



## Troubleshoting

When working on WSL with the submodule Deep-MVLM, if you get the following error:
### Within WSL
```bash
2024-08-16 11:34:12.404 (   1.274s) [    7FD8E5F82740]vtkXOpenGLRenderWindow.:456    ERR| vtkXOpenGLRenderWindow (0xc2dab40): bad X server connection. DISPLAY=localhost:0.0. Aborting.
```

- Install xvfb
```bash
sudo apt-get install xvfb
```
- Screen must be running
```bash
Xvfb :99 -screen 0 1024x768x24 & export DISPLAY=:99
```
- Restart the display manager
```bash
sudo systemctl restart display-manager
```
- Ensure that you have the necessary permission to create UNIX sockets
```bash
sudo chmod 1777 /tmp/.X11-unix
```
### Within Windows
Check if your graphic card driver supports OpenGL on WSL.
Firstly check what graphic cards youre using and update the drivers. E.g. for NVIDIA:
```bash
nvidia-smi
```
Then check if OpenGL is supported:
```bash
glxinfo | grep "OpenGL"
```
If not you can enter the nvidia website and download a driver for WSL.
