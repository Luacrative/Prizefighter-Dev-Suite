bl_info = {
    "name": "Prizefighter Dev Suite",
    "description": "Addon created for Prizefighter's custom animation system.",
    "author": "Luacrative",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "", 
    "doc_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
                "Scripts/My_Script",
    "tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
    "support": "COMMUNITY",
    "category": "View3D",
}

from . import addon

def register():
	addon.register()

def unregister():
	addon.unregister()