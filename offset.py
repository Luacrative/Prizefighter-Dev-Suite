## Dependencies
import bpy, os, zlib, base64, math, mathutils, bpy_extras, re
from mathutils import Vector, Matrix 
from math import degrees

from . import np 

## Variables
bones = {
    "Head",
    "UpperTorso",
    "RightUpperArm",
    "RightLowerArm",
    "RightHand",
    "LeftUpperArm",
    "LeftLowerArm",
    "LeftHand",
    "LowerTorso",
    "RightUpperLeg",
    "RightLowerLeg",
    "RightFoot",
    "LeftUpperLeg",
    "LeftLowerLeg",
    "LeftFoot"
}

first_frame = {} 
second_frame = {}

## Functions
def set_data(context): 
    dict = {} 

    for bone in context.object.pose.bones:
        if not bone.name in bones: continue 
        
        loc = bone.location
        vec = Vector((loc.x, loc.y, loc.z))
        rot = bone.rotation_euler 
        euler = mathutils.Euler((rot.x, rot.y, rot.z), "XYZ")
                
        dict[bone.name] = [vec, euler]

    return dict 

def store_offset(context, type):
    global first_frame 
    global second_frame 

    if type == 1:  
        first_frame = set_data(context)
    else: 
        second_frame = set_data(context)
    
def process_offsets():
    def sub_euler(a, b):
        return mathutils.Euler((a.x - b.x, a.y - b.y, a.z - b.z), "XYZ")

    global first_frame 
    global second_frame 

    offsets = {} 
    
    for bone in second_frame:
        offsetf0 = first_frame[bone]
        offsetf1 = second_frame[bone]
        
        lf0 = offsetf0[0]
        rf0 = offsetf0[1]
        
        lf1 = offsetf1[0]
        rf1 = offsetf1[1]

        l = (lf1 - lf0).freeze()
        r = (sub_euler(rf1, rf0)).freeze()       
        
        if l.x == 0 and l.y == 0 and l.z == 0 and r.x == 0 and r.y == 0 and r.z == 0: continue
        
        lt = (l.x, l.y, l.z)
        rt = (r.x, r.y, r.z)
        
        offsets[bone] = [lt, rt]
    
    np.save("SAVED_OFFSET", offsets)

    return 

def use_offsets(action_name):
    try: 
        offsets = np.load("SAVED_OFFSET")
    except: 
        print("Error loading offsets") 
        return 

    action = bpy.data.actions[action_name] 

    for fcurve in action.fcurves:
        if fcurve.data_path.startswith("pose.bones"):
            try:
                data = fcurve.data_path.split("[", maxsplit=1)[1].split("]", maxsplit=1)
                bone_name = data[0][1:-1]
                keyframe_type = data[1][1:]
                
                if not bone_name in offsets: continue
                if keyframe_type == "scale": continue
                
                index = fcurve.array_index

                if keyframe_type == "location":
                    delta = offsets[bone_name][0][index]
                else:
                    delta = offsets[bone_name][1][index]
                                
                if "Hand" in bone_name or "Foot" in bone_name:
                    global startco 
                    global starthl 
                    global starthr 

                    for frame in fcurve.keyframe_points:
                        if frame.co.x == 0:
                            start = frame
                            startco = start.co.y + delta
                            starthl = start.handle_left.y + delta
                            starthr = start.handle_right.y + delta
                            
                            for frame in fcurve.keyframe_points:
                                frame.co.y = startco
                                frame.handle_left.y = starthl
                                frame.handle_right.y = starthr

                            break      
                else:
                    for frame in fcurve.keyframe_points: 
                        frame.co.y += delta
                        frame.handle_left.y += delta 
                        frame.handle_right.y += delta 
                    
            except IndexError:
                continue