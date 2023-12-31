## Dependencies
import bpy 
import bpy.app

## Main Functions
def show(message = "", title = "Message Box", icon = "INFO"):
    def draw(self, context):
        self.layout.label(text = message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)