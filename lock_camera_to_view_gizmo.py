bl_info = {
    "name": "Lock camera to view gizmo",
    "author": "Miika Puustinen",
    "version": (1, 0, 0),
    "blender": (2, 82, 0),
    "description": "Adds lock camera to view icon while looking through camera.",
    "category": "3d view",
    }

import bpy
from bpy.types import (
    GizmoGroup,
)

class OBJECT_OT_lock_camera_to_view(bpy.types.Operator):
    """Toggle lock camera to view"""
    bl_idname = "object.lock_camera_to_view"
    bl_label = "Lock Camera to View"

    # @classmethod
    # def poll(cls, context):
    #     ob = context.object
    #     return (ob and ob.type == 'CAMERA')

    def execute(self, context):
        lock = bpy.context.space_data.lock_camera

        if lock == False:
            print(lock)
            bpy.context.space_data.lock_camera = True
        else:
            print(lock)
            bpy.context.space_data.lock_camera = False
        return {'FINISHED'}


class Lock_Camera_To_View_Gizmo(GizmoGroup):
    bl_idname = "Lock_Camera_To_View_Gizmo"
    bl_label = "Lock Camera To View Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        return (context.space_data.region_3d.view_perspective == 'CAMERA')

    def draw_prepare(self, context):
        region = context.region

        self.lock_gizmo.matrix_basis[0][3] = region.width - 30
        self.lock_gizmo.matrix_basis[1][3] = region.height - 280

    def setup(self, context):
        mpr = self.gizmos.new("GIZMO_GT_button_2d")
        mpr.icon = 'LOCKED'
        mpr.draw_options = {'BACKDROP', 'OUTLINE'}

        mpr.alpha = 0.4
        mpr.color = 0.1, 0.1, 0.1
        mpr.color_highlight = 0.8, 0.8, 0.8
        mpr.alpha_highlight = 0.4

        mpr.scale_basis = (80 * 0.35) / 2
        self.lock_gizmo = mpr

        mpr.target_set_operator("object.lock_camera_to_view")

        self.camera_widget = mpr

    def refresh(self, context):
        lock = bpy.context.space_data.lock_camera
        mpr = self.camera_widget
        if lock == False:
            mpr.color = 0.1, 0.1, 0.1
        else:
            mpr.color = 0.8, 0.1, 0.1


classes = (OBJECT_OT_lock_camera_to_view, Lock_Camera_To_View_Gizmo,)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
