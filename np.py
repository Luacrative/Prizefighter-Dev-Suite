## Dependencies
import bpy, os
import numpy as numpy

## Variables
directory = (os.path.dirname(os.path.realpath(__file__))) + "/exports/BoneLockConfigs"

## Functions
def get_dir(path):
    path = str(path)

    if "/" in path: 
        process = path.rsplit("/", 1)[-1]
        path = path.replace("/" + process, "")
        folder = directory + "/" + path 

        if not os.path.exists(folder):
            os.makedirs(folder)

        return folder + "/" + process 
    else: 
        return directory + "/" + path 

def save(name, dict):
    dir = get_dir(name) + ".npy"
    numpy.save(dir, dict)
    
def load(name):
    dir = get_dir(name) + ".npy"
    return numpy.load(dir, allow_pickle = "TRUE").item()