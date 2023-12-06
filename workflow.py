## Dependencies
import bpy 

## Main Functions
def update_gloves(self, context, value):
    char_armature = bpy.context.scene.armature     
    if char_armature is None: return

    gloveweld_l = bpy.data.objects["GloveWeld.L"]
    gloveweld_r = bpy.data.objects["GloveWeld.R"]

    for child in gloveweld_l.children:
        if child.name == "LeftGlove": 
            leftglove = child 
            break
        
    for child in gloveweld_r.children:
        if child.name == "RightGlove": 
            rightglove = child 
            break
                
    for child in char_armature.children:
        if child.name == "LeftHand_Geo": 
            lefthand = child 
        elif child.name == "RightHand_Geo":
            righthand = child 

    leftglove.hide_set(not value) 
    rightglove.hide_set(not value) 
    lefthand.hide_set(value)
    righthand.hide_set(value)
    
    return

def update_shorts(self, context, value):   
    char_armature = bpy.context.scene.armature 
    if char_armature is None: return 

    shorts = bpy.data.objects["Shorts"]
    lower_torso = bpy.data.objects["LowerTorso_Geo"]
    right_leg = bpy.data.objects["RightUpperLeg_Geo"]
    right_leg_show = bpy.data.objects["RightUpperLegSHOW"]
    left_leg = bpy.data.objects["LeftUpperLeg_Geo"]
    left_leg_show = bpy.data.objects["LeftUpperLegSHOW"]
    
    shorts.hide_set(not value)
    lower_torso.hide_set(value)
    right_leg.hide_set(value)
    right_leg_show.hide_set(not value)
    left_leg.hide_set(value)
    left_leg_show.hide_set(not value)
    
    return

def update_shoes(self, context, value):
    left_shoe = bpy.data.objects["LeftShoe"]
    left_foot = bpy.data.objects["LeftFoot_Geo"]
    right_shoe = bpy.data.objects["RightShoe"]
    right_foot = bpy.data.objects["RightFoot_Geo"]

    left_shoe.hide_set(not value)
    left_foot.hide_set(value)
    right_shoe.hide_set(not value)
    right_foot.hide_set(value)