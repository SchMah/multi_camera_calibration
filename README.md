# Multi-Camera Calibration Routine

## Overview
This repository contains scripts to calculate the extrinsic parameters (position and orientation) of different cameras in a setup. This method uses calibration pairs (3D world coordinates and matching 2D pixel projects) to compute each camera's position and orientation in a common reference frame. 

## How it works: 
The written script uses the Perspective-n-point (PnP) algorithm available in the OpenCV library [[1]](https://docs.opencv.org/4.x/d5/d1f/calib3d_solvePnP.html)

1. It takes 3D coordinates of a checkerboard and the 2D pixel coordinates of those points in the camera image
2. It finds the best rotation (R) and translation (T) that aligns these 2D-3D pairs by minimizing the reprojection error.
3. Finally, it generates a JSON file containing the rotation matrix (R) and translation vector (T) for each camera


## Getting the code
Clone this repository to your local system or download the source code and navigate to the directory it is saved in. 
```bash
git clone https://github.com/SchMah/multi_camera_calibration.git
cd PATH/TO/PROJECT/FOLDER
```
## Setup the environment
You can either use conda or Python's built in venv.

### Option 1 (Using conda)
Requirements: Anaconda installed. 

You can replace `mul_cam_cal` with another name for your virtual environment

```bash 
# create a conda environment
conda create -n mul_cam_cal python=3.11 pip

#activate conda
conda activate mul_cam_cal
```

Install the required packages:
```bash
pip install -r requirements.txt
```

### Option 2 (Using venv)
Requirements: Python 3.11 installed

Create a virtual environment: 
`mul_cam_cal` is the name of the virtual environmnet. Conventionally, you can choose `venv`

```bash 
Python3 -m venv mul_cam_cal
```
Activate the virtual enviornmnet: 
```bash
source mul_cam_cal/bin/activate
```

Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage
### Running the script

Run the script from the command line: 
The script expects the following files : 
- `intrinsics.json` camera intrinsics (K, distortion, resolution)
- `observations.json` 3D-2D checkerboard correspondence

You can either run the following command in the terminal. It will use `intrinsics.json` and `observations.json` stored in the project folder as input and save the output as `extrinsics.json`
  
```python
python extrinsics.py 
```
or 

```python
python extrinsics.py /PATH/TO/YOUR/intrinsics.json /PATH/TO/YOUR/observations.json
```

By default, the output is saved under "extrinsics.json". You can specify a custom output filename using: 

```python
python extrinsics.py /PATH/TO/YOUR/intrinsics.json /PATH/TO/YOUR/observations.json /PATH/TO/YOUR/OUT_FILENAME.json
```

## Output
A JSON file containing the extrinsics for each camera: 
- 'R' (Rotation matrix) : `3 * 3` matrix defining camera orientation 
- 'T' (Traslation Vector) : `3 * 1` vector defining camera position in meters. 

```json
{
    "cam0": {
        "R": [
            [ ],
            [ ],
            [ ]
        ],
        "T": [ ]
    },
    "cam1": {
            
```