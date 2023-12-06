## Dependencies
import bpy
import bpy.utils.previews 
from bpy.utils import register_class, unregister_class 
from bpy.types import Operator, Panel 
import os 
import subprocess

import webbrowser

from . import exportanim 
from . import workflow 
from . import lockpose 
from . import offset 
from . import ui 

## Variables
icon_images = {} 
images = [ 
    "save",
    "load",
    "clear",
    "drive"
]

## Functions
def get_image(name):
    pcoll = icon_images["main"]
    return pcoll[name].icon_id

## Classes
class PFSUITE_export_anim(Operator):
    """ Export Current Animation """
    bl_idname = "export.operator"
    bl_label = "Export Current Animation"

    @classmethod
    def poll(cls, context):
        return context.mode == "POSE"

    def execute(self, context): 
        armature = context.scene.armature 
        if armature is None: 
            ui.show("No loaded armature")
        else: 
            exportanim.export_action(armature, armature.animation_data.action)
            ui.show("Exported current animation")

        return {"FINISHED"}

class PFSUITE_batch_export(Operator):
    """ Export All Animations """
    bl_idname = "batch.operator"
    bl_label = "Export All Animations"

    @classmethod
    def poll(cls, context):
        return context.mode == "POSE"

    def execute(self, context): 
        armature = context.scene.armature 
        if armature is None: 
            ui.show("No loaded armature")
        else: 
            exportanim.batch_export_actions(armature)
            ui.show("Exported all animations")

        return {"FINISHED"}

class PFSUITE_lockpose_create_lock(Operator):
    """ Create New Lock"""
    bl_idname = "createlock.operator"
    bl_label = "Create New Lock in Lock Pose System"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if context.mode == "POSE":
            selected_bones = bpy.context.selected_pose_bones

            if selected_bones is None or len(selected_bones) == 0:
                return False 
            else: 
                return True 

        return False 

    def execute(self, context): 
        armature = context.scene.armature 
        if armature is None: 
            ui.show("No loaded armature")
        else: 
            lockpose.create_lock(armature)
        
        return {"FINISHED"}

class PFSUITE_lockpose_connect_lock(Operator):
    """ Connect New Lock """
    bl_idname = "connectlock.operator"
    bl_label = "Connect Lock in Lock Pose System"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if context.mode == "POSE":
            selected_bones = bpy.context.selected_pose_bones

            if selected_bones is None or len(selected_bones) == 0:
                return False 
            else: 
                return True 

        return False 
    
    def execute(self, context): 
        armature = context.scene.armature 
        if armature is None: 
            ui.show("No loaded armature")
        else: 
            lockpose.connect_lock(armature, float(context.scene.influence) / 100)
        
        return {"FINISHED"}
    
class PFSUITE_lockpose_save(Operator):
    """ Save Locks """
    bl_idname = "savelock.operator"
    bl_label = "Save Locks as .npy"

    @classmethod 
    def poll(cls, context):
        if context.mode == "POSE":
            armature = context.scene.armature 
            if armature is None: 
                return False 

            bones = armature.pose.bones
            foundcon = False 

            for bone in bones: 
                if bone.constraints:
                    for _ in bone.constraints:
                        foundcon = True 
                        
                        break 
            
            if foundcon: 
                return True 
        else: 
            return False 

        #return context.mode == "POSE"

    def execute(self, context):
        armature = context.scene.armature 
        if armature is None: 
            ui.show("No loaded armature")
        else: 
            lockpose.save_locks(armature, context.object.animation_data.action, False)
            ui.show("Saved config")

        return {"FINISHED"} 

class PFSUITE_lockpose_clear(Operator):
    """ Clear Locks"""
    bl_idname = "clearlock.operator"
    bl_label = "Clear .npy Locks"

    @classmethod 
    def poll(cls, context):
        if context.mode == "POSE":
            armature = context.scene.armature 
            if armature is None: 
                return False 

            bones = armature.pose.bones
            foundcon = False 

            for bone in bones: 
                if bone.constraints:
                    for constraint in bone.constraints:
                        foundcon = True 
                        break 
            
            if foundcon: 
                return True 
        else: 
            return False 

        #return context.mode == "POSE"

    def execute(self, context):
        armature = bpy.context.scene.armature 
        if armature is None: 
            ui.show("No loaded armature")
        else: 
            lockpose.clear_locks(armature)
            ui.show("Cleared config")

        return {"FINISHED"} 

class PFSUITE_lockpose_load(Operator):
    """ Load Locks"""
    bl_idname = "loadlock.operator"
    bl_label = "Load .npy Lock"

    @classmethod 
    def poll(cls, context):
        return context.mode == "POSE"

    def execute(self, context):
        armature = bpy.context.scene.armature 
        if armature is None: 
            ui.show("No loaded armature")
        else: 
            lockpose.load_locks(armature, context.object.animation_data.action)
            ui.show("Loaded config")

        return {"FINISHED"} 


class PFSUITE_offset_setone(Operator):
    """ Set First Offset """
    bl_idname = "setoffsetone.operator"
    bl_label = "Set First Offset"

    @classmethod 
    def poll(cls, context):
        return context.mode == "POSE"

    def execute(self, context):
        offset.store_offset(context, 1)
        ui.show("First frame set")

        return {"FINISHED"}

class PFSUITE_offset_settwo(Operator):
    """ Set Second Offset """
    bl_idname = "setoffsettwo.operator"
    bl_label = "Set Second Offset"

    @classmethod 
    def poll(cls, context):
        return context.mode == "POSE"

    def execute(self, context):
        offset.store_offset(context, 2)
        ui.show("Second frame set")

        return {"FINISHED"}

class PFSUITE_offset_calculate(Operator):
    """ Calculate and Store Offsets """
    bl_idname = "calculateoffset.operator"
    bl_label = "Calculate and Store Offsets"

    @classmethod 
    def poll(cls, context):
        return context.mode == "POSE"

    def execute(self, context):
        offset.process_offsets()
        ui.show("Calculated and stored offsets")

        return {"FINISHED"}

class PFSUITE_offset_apply(Operator):
    """ Apply Offsets """
    bl_idname = "applyoffsets.operator"
    bl_label = "Apply Offsets"

    @classmethod 
    def poll(cls, context):
        return context.mode == "POSE"

    def execute(self, context):
        action_name = context.object.animation_data.action.name 

        offset.use_offsets(action_name)
        ui.show("Offsets applied")

        return {"FINISHED"}

class PFSUITE_open_drive(Operator):
    """ Open Drive """
    bl_idname = "opendrive.operator"
    bl_label = "Open Drive"

    def execute(self, context):
        try_browsers = {
            "chrome": [
                "chrome",
                "--chrome-frame",
                "--window-size=800,600",
                "--window-position=240,80",
                "--app=%s &",
            ],
        }
        try_browsers["chromium"] = try_browsers["chrome"][:]
        try_browsers["chromium"][0] = 'chromium'
        URL = "https://drive.google.com/drive/u/0/folders/1uy1BCK-fJYHkPoIULptYG3r-_Lpu7W_L"

        for browser in try_browsers.values():
            if webbrowser.get(" ".join(browser)).open(URL):
                break
        else:
            webbrowser.open(URL)

        return {"FINISHED"}

class PFSUITE_open_addon(Operator):
    """ Open Addon"""
    bl_idname = "openaddon.operator"
    bl_label = "Open Addon"

    def execute(self, context):
        folder = (os.path.dirname(os.path.realpath(__file__)))

        #subprocess.Popen(rf'explorer /select,"{folder}"')
        os.startfile(folder + "/exports")


        return {"FINISHED"}


class PFSUITE_sidebar(Panel):
    """Prizefighter Dev Suite Panel"""
    bl_label = "Prizefighter Dev Suite"
    bl_space_type = "VIEW_3D"
    #bl_region_type = "HEADER"
    bl_region_type = "UI"
    bl_category = "Prizefighter Suite"
    
    def draw(self, context):        
        cwm = context.window_manager
        
        self.layout.prop(context.scene, "armature", text = "Source", icon = "ARMATURE_DATA")
        self.layout.separator()

        ##
        box = self.layout.box()
        box.label(text = "Export Animations")
        #self.layout.label(text = "Export Animations")
        
        col = box.column(align = True)
        col.operator(PFSUITE_export_anim.bl_idname, text = "Current Animation")
        col.operator(PFSUITE_batch_export.bl_idname, text = "All Animations")
        ##
        
        ##        
        box2 = self.layout.box()
        box2.label(text = "Lock Animation Poses")

        col2 = box2.column(align = True)
        col2.operator(PFSUITE_lockpose_create_lock.bl_idname, icon = "LOCKED", text = "Create Lock")

        row = box2.row(align = True)
        row.prop(context.scene, "influence", slider = True)
        row.operator(PFSUITE_lockpose_connect_lock.bl_idname, text = "Connect")
        
        box2.separator() 

        col2b = box2.column(align = True)
        col2b.operator(PFSUITE_lockpose_save.bl_idname, icon_value = get_image("save"), text = "Save Config")
        col2b.operator(PFSUITE_lockpose_load.bl_idname, icon_value = get_image("load"), text = "Load Config")
        col2b.operator(PFSUITE_lockpose_clear.bl_idname, icon_value = get_image("clear"), text = "Clear Config")
        ##

        ##        
        box3 = self.layout.box()

        row3 = box3.row(align = True)
        row3.label(icon = "FF", text = "")

        """
        def make_fps_button(fps):
            button = row3.operator(PFSUITE_change_fps.bl_idname, text = fps)
            button.fps = int(fps)
        
        fps_buttons = ["5", "10", "30", "45", "60"]
        
        for fps in fps_buttons:
           make_fps_button(fps)
        """

        row3.prop(context.scene, "fps", text = "Frames / Second", slider = True)

        row3b = box3.row(align = True)   
        row3b.label(icon = "HIDE_OFF", text = "")
        
        row3b.prop(cwm, "gloves_shown", text = "Gloves", toggle = True)
        row3b.prop(cwm, "shorts_shown", text = "Shorts", toggle = True)  
        row3b.prop(cwm, "shoes_shown", text = "Shoes", toggle = True) 
        
        box4 = self.layout.box() 
        box4.label(text = "Offset System")

        row4 = box4.row(align = True)
        row4.operator(PFSUITE_offset_setone.bl_idname, text = "Set 1st")
        row4.operator(PFSUITE_offset_settwo.bl_idname, text = "Set 2nd")

        row5 = box4.row(align = True)
        row5.operator(PFSUITE_offset_calculate.bl_idname, text = "Calculate")
        row5.operator(PFSUITE_offset_apply.bl_idname, text = "Apply") 

        self.layout.separator()

        row6 = self.layout.row(align = True)
        row6.operator(PFSUITE_open_drive.bl_idname, icon_value = get_image("drive"), text = "Drive")
        row6.operator(PFSUITE_open_addon.bl_idname, icon = "FILE_FOLDER", text = "Exports")

        self.layout.separator()
        self.layout.label(text = "// Luacrative")

    @staticmethod
    def add_menu():
        PFSUITE_sidebar.remove_menu()
        PFSUITE_sidebar._menu_original = bpy.types.VIEW3D_MT_editor_menus.draw_collapsible

        def menu(context, layout):
            PFSUITE_sidebar._menu_original(context, layout)

            row = layout.row(align = True)
            
            row.popover(panel = "PFSUITE_sidebar", text = PFSUITE_sidebar.bl_label)
    
        bpy.types.VIEW3D_MT_editor_menus.draw_collapsible = menu

    @staticmethod 
    def remove_menu():
        if not hasattr(PFSUITE_sidebar, "_menu_original"): return
        
        bpy.types.VIEW3D_MT_editor_menus.draw_collapsible = PFSUITE_sidebar._menu_original
        del PFSUITE_sidebar._menu_original

## Header 
classes = [
    PFSUITE_export_anim,
    PFSUITE_batch_export,
    
    #PFSUITE_change_fps,

    PFSUITE_lockpose_create_lock,
    PFSUITE_lockpose_connect_lock,
    PFSUITE_lockpose_clear,
    PFSUITE_lockpose_save, 
    PFSUITE_lockpose_load,

    PFSUITE_offset_setone,
    PFSUITE_offset_settwo,
    PFSUITE_offset_calculate,
    PFSUITE_offset_apply,

    PFSUITE_open_drive,
    PFSUITE_open_addon,

    PFSUITE_sidebar,
]

## Main

def register():    
    pcoll = bpy.utils.previews.new() 
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    for img in images: 
        pcoll.load(img, os.path.join(icons_dir, img + ".png"), "IMAGE")
    icon_images["main"] = pcoll 


    bpy.types.WindowManager.gloves_shown = bpy.props.BoolProperty(
        default = False,
        update = lambda self, context: workflow.update_gloves(self, context, self.gloves_shown)
    )
    
    bpy.types.WindowManager.shorts_shown = bpy.props.BoolProperty(
        default = False,
        update = lambda self, context: workflow.update_shorts(self, context, self.shorts_shown)
    )
    
    bpy.types.WindowManager.shoes_shown = bpy.props.BoolProperty(
        default = False,
        update = lambda self, context: workflow.update_shoes(self, context, self.shoes_shown)
    )
    
    bpy.types.Scene.armature = bpy.props.PointerProperty(
		type = bpy.types.Object,
		poll = lambda self, object: object.type == "ARMATURE",
	)

    bpy.types.Scene.influence = bpy.props.IntProperty(
        name = "%", 
        default = 50, 
        soft_max = 100, 
        soft_min = 0
    )

    def update_fps(context):
        context.scene.render.fps = int(context.scene.fps)

    bpy.types.Scene.fps = bpy.props.IntProperty(
        name = "fps",
        default = 60, 
        soft_max = 60,
        soft_min = 5,
        step = 5,
        update = lambda self, context: update_fps(context)
    )


    for c in classes:
        bpy.utils.register_class(c)

    #PFSUITE_sidebar.add_menu()
        
def unregister():
    for pcoll in icon_images.values(): 
        bpy.utils.previews.remove(pcoll)
    icon_images.clear() 

        
    del bpy.types.WindowManager.shorts_shown
    del bpy.types.WindowManager.gloves_shown
    del bpy.types.WindowManager.shoes_shown
    del bpy.types.Scene.armature
    del bpy.types.Scene.influence
    del bpy.types.Scene.fps 

    #PFSUITE_sidebar.remove_menu()

    for c in classes:
        bpy.utils.unregister_class(c)