## Dependencies
import bpy, os, zlib, base64, math, re, json, bpy_extras, time 
from bpy.utils import register_class, unregister_class 
from bpy.types import Operator 
from bpy.types import Panel
from itertools import chain
from mathutils import Vector, Matrix
from bpy_extras.io_utils import ImportHelper
from bpy.props import *

from math import degrees

from . import lockpose 
from . import ui 

## Variables
directory = (os.path.dirname(os.path.realpath(__file__))) + "/exports/Animations" #os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop") 
transform_to_blender = bpy_extras.io_utils.axis_conversion(from_forward = "Z", from_up = "Y", to_forward = "Y", to_up = "Z").to_4x4()

bone_codes = {
    "LowerTorso": "LT",
    "UpperTorso": "UT",
    "Head": "H",
    
    "RightUpperLeg": "RUL",
    "RightLowerLeg": "RLL",
    "RightFoot": "RF",
    
    "LeftUpperLeg": "LUL",
    "LeftLowerLeg": "LLL",
    "LeftFoot": "LF",
    
    "RightUpperArm": "RUA",
    "RightLowerArm": "RLA",
    "RightHand": "RH",
    
    "LeftUpperArm": "LUA",
    "LeftLowerArm": "LLA",
    "LeftHand": "LH",
}

tab = "    "


## Functions 
def trunctuate(number, decimals):
    trunct = f"%.{decimals}f"%(number)
    trunct = trunct.rstrip("0")
    
    if trunct == "-0." or trunct == "0.": trunct = "0"
    if trunct == "-1." or trunct == "1.": trunct = "1"
    if trunct == "-2." or trunct == "2.": trunct = "2"
    
    return trunct

def mat_to_cf(mat):
    cf = [
        mat[0][3], mat[1][3], mat[2][3],
        mat[0][0], mat[0][1], mat[0][2],
        mat[1][0], mat[1][1], mat[1][2],
        mat[2][0], mat[2][1], mat[2][2]
    ]

    return cf

def normalize_rot(cf): 
    rot = [ 
       cf[3], -cf[4], cf[5], -cf[6], cf[7], -cf[8], cf[9], -cf[10], cf[11] 
    ] 
    
    return rot 

def get_bone_cf(bone):
    back_trans = transform_to_blender.inverted()

    parent_obj_transform = back_trans @ (bone.parent.matrix @ Matrix())
    parent_orig_base_mat = back_trans @ (Matrix() @ Matrix())

    orig_transform = parent_orig_base_mat.inverted() @ back_trans @ (Matrix() @ Matrix())
    cur_transform = parent_obj_transform.inverted() @ back_trans @ (bone.matrix @ Matrix())
    bone_transform = orig_transform.inverted() @ cur_transform

    return mat_to_cf(bone_transform)

def get_keyframes():
    index = 0
    keyframes = []
    
    bpy.ops.screen.frame_jump(end = False)
    
    while True:
        status = bpy.ops.screen.keyframe_jump(next = True)
        
        if status != {"FINISHED"}:
            break
        else:
            keyframes.insert(index, bpy.context.scene.frame_current)
        
        index +=1 
        
    return keyframes

def export_action(armature, action):   
    first_keyframe = bpy.context.scene.frame_start #int(action.frame_range[0]) 
    last_keyframe = int(action.frame_range[1]) #bpy.context.scene.frame_end 
    frame_range = range(first_keyframe, last_keyframe)
    
    frame_set = bpy.context.scene.frame_set
    frame_set(0)

    loaded_locks = lockpose.load_locks(armature, action)
    anim_data = "local C = CFrame.new; local A = CFrame.Angles; return {\n" + tab + "Speed = 1;\n" + tab + "Order = 1;\n" + tab + "Looped = false;\n" + tab + "Mirrored = nil;\n" + tab + "IsOffset = nil;\n\n" + tab + "Keyframes = {\n"

    duplicate = action.copy()
    armature.animation_data.action = duplicate   
    bpy.ops.nla.bake(frame_start = first_keyframe, frame_end = last_keyframe, only_selected = False, visual_keying = True, clear_constraints = True, clear_parents = True, use_current_action = True, clean_curves = True, bake_types = {"POSE"})

    bones_keyed = [] 
    bones_queue = {} 

    for fcurve in action.fcurves:
        name = fcurve.group.name
        
        if name in bones_keyed: continue 
        
        bones_keyed.append(name)

        if "Lock" in name or name == "Root" or name == "HumanoidRootNode": continue  
        if "Thumb" in name or "Pinky" in name or "Ring" in name or "Middle" in name or "Index" in name: continue 

        bones_queue[bone_codes[name]] = armature.pose.bones[name]

    bones_data = {} 
    for bone_code in bones_queue: 
        bones_data[bone_code] = {}

    for frame in frame_range: 
        frame_set(frame)
        
        for bone_code, bone in bones_queue.items():
            t_loc = bone.location
            lx = trunctuate(-t_loc.x, 4)
            ly = trunctuate(t_loc.y, 4)
            lz = trunctuate(-t_loc.z, 4)
            no_loc = lx == "0" and ly == "0" and lz == "0"
            
            bone_cf = get_bone_cf(bone) 
            rot = normalize_rot(bone_cf)
            
            rx = str(trunctuate(math.atan2(-rot[5], rot[8]), 4))
            ry = str(trunctuate(math.asin(rot[2]), 4))
            rz = str(trunctuate(math.atan2(-rot[1], rot[0]), 4))
            no_rot = rx == "0" and ry == "0" and rz == "0"
            
            location = "C()" if no_loc else "C(" + lx + "," + ly + "," + lz + ")"
            rotation = "" if no_rot else " * A(" + rx + "," + ry + "," + rz + ")"    
            transform = location + rotation

            bones_data[bone_code][frame] = transform 

    for bone_code, frames in bones_data.items(): 
        anim_data += tab*2 + '["' + bone_code + '"] = {\n'

        frame_len = len(frames) - 1

        for frame in frames: 
            transform = frames[frame] 

            anim_data += tab*3 + transform + ";\n"

            if frame == frame_len:
               anim_data += tab*3 + transform + ";\n" + tab*2 + "};\n"
       
    anim_data += tab + "}\n}"
    
    ## Locate Directory
    if "/" in action.name: 
        process = action.name.rsplit("/", 1)[-1]
        path = action.name.replace("/" + process, "")
        folder = f"{directory}/{path}" 

        if not os.path.exists(folder):
            os.makedirs(folder)

        file = open(f"{folder}/{process}.txt", "w")
    else: 
        file = open(f"{directory}/{action.name}.txt", "w")

    ## Write to file 
    file.write(anim_data)
    file.close()

    bpy.context.scene.frame_set(0)

    if loaded_locks == True: 
        lockpose.clear_locks(armature)

    bpy.data.actions.remove(duplicate) 
    armature.animation_data.action = action 

def batch_export_actions(armature):
    for action in bpy.data.actions:
        export_action(armature, action)    