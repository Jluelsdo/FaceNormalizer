Package to normalize a 3D human face, in orientation, location and number of verticies. It is used to normalize the face before feeding it to a neural network.

## Installation

To install the submodules after cloning run
``` git submodule update --init --recursive ```
To install the requirements run
``` pip install -r requirements.txt ```

## Config.json
Within the config.json the user can specify the order of manipulation and the parameters for each manipulation.
The following is an example of a config.json file:

```json
{
    "Order of Manipulation": [
        "Cut face",
        "Rescale size",
        "Rotate face",
        "Translate face",
        "Add noise",
        "Normalize number of vertices"
    ],
    "Normalize number of verticies": {
        "Number of Vertices": 1000
    }
}
```


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
