BPY_IMPORT = "import bpy"
DESELECT_ALL = "bpy.ops.object.select_all(action='DESELECT')"
SELECT_CAMERA = 'bpy.data.objects["Camera"].select_set(True)'

ADD_CAMERA_TRACKING_TO_OBJECT = "bpy.ops.object.constraint_add(type='TRACK_TO')"
SET_CAMERA_TRACKING_TO_TARGET = 'bpy.context.object.constraints["Track To"].target = bpy.data.objects["Target"]'

APPLY_AUTO_KEYFRAMES = "bpy.context.scene.tool_settings.use_keyframe_insert_auto = True"
APPLY_LOCATION = "bpy.ops.anim.keyframe_insert_menu(type='Location')"

SET_KEYFRAME = "bpy.context.scene.frame_current = {val:d}"
SET_START_KEYFRAME = "bpy.context.scene.frame_start = {val:d}"
SET_END_KEYFRAME = "bpy.context.scene.frame_end = {val:d}"

ABSOLUTE_POSITION_X = "bpy.context.object.location[0] = {val:4.2f}"
ABSOLUTE_POSITION_Y = "bpy.context.object.location[1] = {val:4.2f}"
ABSOLUTE_POSITION_Z = "bpy.context.object.location[2] = {val:4.2f}"
