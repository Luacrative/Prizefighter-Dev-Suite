## Dependencies
import bpy 
import bpy.app
import os 

from . import np 
from . import ui 

## Variables 
save_data = {} 

desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop") 

## Functions
def create_lock(armature):
    selected_bones = bpy.context.selected_pose_bones
    bones = armature.pose.bones 

    if selected_bones is None or len(selected_bones) == 0: 
        ui.show("No selected bones to copy")
        return
    
    for bone in selected_bones:
        bone.bone.select = False
    
    for bone in selected_bones: 
        if "Lock" in bone.name: continue 

        print("Creating lock for " + bone.name)

        index = bone.name + "Lock"
        
        bpy.ops.object.mode_set(mode = "EDIT")
        
        if index in bones: 
            old_copy = armature.data.edit_bones[index]
            armature.data.edit_bones.remove(old_copy)

        edit_bone = armature.data.edit_bones[bone.name]

        copy = armature.data.edit_bones.new(index)
        copy.length = edit_bone.length
        copy.head = edit_bone.head
        copy.head_radius = edit_bone.head_radius 
        copy.tail = edit_bone.tail
        copy.tail_radius = edit_bone.tail_radius 
        copy.matrix = edit_bone.matrix.copy()

        bpy.ops.object.mode_set(mode = "POSE")

        pose_copy = bones[index]

        pose_copy.rotation_mode = "XYZ"
        pose_copy.matrix = bone.matrix.copy()

        bpy.context.object.data.bones.active = pose_copy.bone 
        pose_copy.bone.select = True 
        bpy.ops.pose.hide(unselected = False)
        pose_copy.bone.select = False  

    
        ui.show("Created lock for " + bone.name)
    
    bpy.ops.object.mode_set(mode = "POSE")
    
    for bone in selected_bones:
        bone.bone.select = True 
        bpy.context.object.data.bones.active = bone.bone 

def connect_lock(armature, influence):
    selected_bones = bpy.context.selected_pose_bones
    bones = armature.pose.bones 
    
    if selected_bones is None or len(selected_bones) == 0: 
        print("No selected bones to connect")
        return
    
    if influence == 0.0:
        for bone in selected_bones:
            if "Lock" in bone.name: continue 
            
            lock_index = bone.name + "Lock"
            if not lock_index in bones: continue 

            for constraint in bone.constraints:
                if constraint.type == "COPY_TRANSFORMS":
                    bone.constraints.remove(constraint)
        
        return 
    
    for bone in selected_bones: 
        if "Lock" in bone.name: continue 
        
        lock_index = bone.name + "Lock"
        if not lock_index in bones: continue 
        
        for constraint in bone.constraints:
            if constraint.type == "COPY_TRANSFORMS":
                bone.constraints.remove(constraint)
        
        copy_trans = bone.constraints.new("COPY_TRANSFORMS")
        copy_trans.target = armature 
        copy_trans.subtarget = lock_index 
        copy_trans.target_space = "WORLD"
        copy_trans.owner_space = "WORLD"
        copy_trans.influence = influence

def save_locks(armature, action, Clear):
    bones = armature.pose.bones 

    global save_data 
 
    for bone in bones: 
        if bone is None: continue 

        for constraint in bone.constraints:
            if constraint is None: 
                print("Constraint is none!")
                continue 

            try: 
                if constraint.type: 
                    if constraint.type == "COPY_TRANSFORMS":
                        save_data[bone.name] = float(constraint.influence)
                else: 
                    print("Constraint has no type!")
                    ui.show("Failed to save one or more constraints") 
            except: 
                ui.show("Failed to save one or more constraints")

    if len(save_data) >0: 
        np.save(action.name, save_data)

    if Clear == True: 
        clear_locks()  

    save_data = {} 

def clear_locks(armature):
    bones = armature.data.edit_bones

    bpy.ops.object.mode_set(mode = "EDIT")

    for bone in bones: 
        if "Lock" in bone.name: 
            bones.remove(bone)

    bpy.ops.object.mode_set(mode = "POSE")
    pose_bones = armature.pose.bones

    for bone in pose_bones: 
        for constraint in bone.constraints:
            if constraint.type == "COPY_TRANSFORMS":
                bone.constraints.remove(constraint)
    

def load_locks(armature, action):
    try:
        data = np.load(action.name)
    except:
        print("Error when loading locks for " + action.name)
        return False 

    selected_bones = bpy.context.selected_pose_bones
    bones = armature.pose.bones 
    
    for bone in selected_bones: 
       bone.bone.select = False  
 
    for bone in bones: 
        if not bone.name in data: continue 

        influence = data[bone.name] 
        index = bone.name + "Lock"

        bpy.ops.object.mode_set(mode = "EDIT")
        
        if index in bones: 
            old_copy = armature.data.edit_bones[index]
            
            armature.data.edit_bones.remove(old_copy)

        edit_bone = armature.data.edit_bones[bone.name]

        copy = armature.data.edit_bones.new(index)
        copy.length = edit_bone.length
        copy.head = edit_bone.head
        copy.head_radius = edit_bone.head_radius 
        copy.tail = edit_bone.tail
        copy.tail_radius = edit_bone.tail_radius 
        copy.matrix = edit_bone.matrix.copy()

        bpy.ops.object.mode_set(mode = "POSE")

        pose_copy = bones[index]

        pose_copy.rotation_mode = "XYZ"
        pose_copy.matrix = bone.matrix.copy()

        bpy.context.object.data.bones.active = pose_copy.bone 
        pose_copy.bone.select = True 
        bpy.ops.pose.hide(unselected = False)
        pose_copy.bone.select = False  

        for constraint in bone.constraints:
            if constraint.type == "COPY_TRANSFORMS":
                bone.constraints.remove(constraint)
        
        copy_trans = bone.constraints.new("COPY_TRANSFORMS")
        copy_trans.target = armature 
        copy_trans.subtarget = index 
        copy_trans.target_space = "WORLD"
        copy_trans.owner_space = "WORLD"
        copy_trans.influence = influence
    
    return True 