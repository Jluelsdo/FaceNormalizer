Package to normalize a 3D human face, in orientation, location and number of verticies. It is used to normalize the face before feeding it to a neural network.


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
