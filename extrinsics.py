import numpy as np
import json
import cv2
import sys
from pathlib import Path

import config

base_dir = Path(__file__).resolve().parent

print("---")

def load_data(intrinsics_file, observations_file):
    """
    Loads JSON configuration files for intrinsics and observations.

    Args : intrinsics_file, observations_file 

    Returns: intrinsics and observation as dictionaries  
             if no file is found, retun None
    """
    try:
        with open(intrinsics_file,"r") as file:
            intrinsics = json.load(file)
            print("Loaded intrinsics JSON file")
            print("---")
        with open(observations_file,"r") as file:
            observation = json.load(file)
            print("Loaded observations JSON file")
            print("---")
            return intrinsics, observation
            
    except FileNotFoundError as err:
        print (f"Err: Required file '{err.filename}' not found")
        return None, None
        
    except json.JSONDecodeError as err_dec:
        print(f"Err: Failed to decode JSON from file {err_dec.filename}, check the file format")
        return None, None



def cal_extrinsics(intrinsics, observations):
    """
    This function calculates the extrinsic camera parameters (Rotation matrix, Translation vector)
    using the Perspective-n-Point algorithm in openCV. 

    Args: intrinsics (dict), observations (dicts)
    
    Return: A dictionary containing 'R' (Rotation matrix), 'T' (Translation vector) for each camera
    
    """
    extrinsics_output = {}

    # iterate over all cameras found in the observation file 
    for cam_n, obs_data in observations['cameras'].items():
        print(f"Found {cam_n} in observations")
        print("---")
        # --------------------------------------------------------------
        ##### Load world and image points (3dpoints(objects: checkerboard points) and 2dpoints(images)) ######
        # --------------------------------------------------------------
        
        # 3D world coordinates, in meters
        # "location of the calibration checkerboard's vertices in 3d space, units of meters)"
        three_d_points_obj = np.array(obs_data['points_3d'], dtype = np.float64)

        # 2D image points, in pixels
        # "location of the calibration checkerboard's vertices in the 2d image"
        two_d_points_img = np.array(obs_data['points_2d'], dtype = np.float64)

        # --------------------------------------------------------------
        ##### Load intrinsics parameters, 'K' and distortion coefficients #####
        # --------------------------------------------------------------
        
        # load calibration matrix 'K' from given intrinsics data 
        K = np.array(intrinsics[cam_n]["K"], dtype = np.float64 )

        # load distortion coefficients from given intrinsics data 
        dist_coeff = np.array(intrinsics[cam_n]["distortion"], dtype = np.float64 )

        # --------------------------------------------------------------
        ##### solve PnP 
        # --------------------------------------------------------------
       
        success, rotation_vector, translation_vector = cv2.solvePnP(
            three_d_points_obj, two_d_points_img, K, dist_coeff, flags = cv2.SOLVEPNP_ITERATIVE)
        
        # --------------------------------------------------------------
        ##### Convert rotation vector to rotation matrix and store results
        # --------------------------------------------------------------
        # 
        if success:
            # convert rotation vector to rotation matrix using Rodrigues
            R, _ = cv2.Rodrigues(rotation_vector)
            
            print(f"Computed extrinsics parameters for camera '{cam_n}'")
            print("---")

            # store results as list
            extrinsics_output[cam_n] = {
                "R" : R.tolist(),
                "T" : translation_vector.flatten().tolist()
            }
        else:
            print("solvePnP failed to find a solution.")
            print("---")

                                

    return extrinsics_output



if __name__ == '__main__':

    # -----------  handling input arguments ------------
    file_n = sys.argv[1:]
    n_args = len(file_n)
    if n_args == 0: 
        intrinsics_file = config.FILE_INTRINSICS
        observations_file = config.FILE_OBSERVATION 
        output_file = config.OUTPUT_FILENAME
    elif n_args == 2:
        intrinsics_file = file_n[0]
        observations_file = file_n[1]  
        output_file = config.OUTPUT_FILENAME
    elif n_args >= 3:
        intrinsics_file = file_n[0]
        observations_file = file_n[1]
        output_file = file_n[2]
    else: 
        print("Usage Error, python extrinsics.py <intrinsics.json> <observation.json> [output_filename]")
        sys.exit(1)
        
    intrinsics_file = Path(intrinsics_file)
    observations_file = Path(observations_file)
    output_file = Path(output_file)

    # -------------- load data ---------------
    intrinsics, observations = load_data(intrinsics_file,observations_file)

    if intrinsics is None or observations is None:
        sys.exit(1)
    #------------- calculate extrinsics parameters -------
    if intrinsics and observations:
        extrinsics_output = cal_extrinsics(intrinsics, observations)
        
    # save results:     
    if extrinsics_output:  
        output_file.parent.mkdir(parents= True, exist_ok = True)
        with open(output_file, "w") as file: 
            json.dump(extrinsics_output,file, indent = 4)
            print(f"Saved results as a .json file {output_file.resolve()}")

            