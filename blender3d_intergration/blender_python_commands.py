from enum import StrEnum


class BlenderPythonCommands(StrEnum):
    BPY_IMPORT = "import bpy"
    SELECT_ALL = "bpy.ops.object.select_all(action='SELECT')"
    DESELECT_ALL = "bpy.ops.object.select_all(action='DESELECT')"
    SELECT_CAMERA = 'bpy.data.objects["Camera"].select_set(True)'
    SELECT_CAMERA_PATH = 'bpy.data.objects["CameraPath"].select_set(True)'

    ADD_CAMERA_TRACKING_TO_OBJECT = "bpy.ops.object.constraint_add(type='TRACK_TO')"
    SET_CAMERA_TRACKING_TO_TARGET = 'bpy.context.object.constraints["Track To"].target = bpy.data.objects["Target"]'

    APPLY_AUTO_KEYFRAMES = "bpy.context.scene.tool_settings.use_keyframe_insert_auto = True"
    APPLY_LOCATION = "bpy.ops.anim.keyframe_insert_menu(type='Location')"
    APPLY_SCALING = "bpy.ops.anim.keyframe_insert_menu(type='Scaling')"

    SET_FRAME = "bpy.context.scene.frame_set({val:d})"
    SET_START_FRAME = "bpy.context.scene.frame_start = {val:d}"
    SET_END_FRAME = "bpy.context.scene.frame_end = {val:d}"

    ABSOLUTE_POSITION_X = "bpy.context.object.location[0] = {val:4.2f}"
    ABSOLUTE_POSITION_Y = "bpy.context.object.location[1] = {val:4.2f}"
    ABSOLUTE_POSITION_Z = "bpy.context.object.location[2] = {val:4.2f}"

    SCALE_X = "bpy.context.object.scale[0] = {val:4.2f}"
    SCALE_Y = "bpy.context.object.scale[1] = {val:4.2f}"
    SCALE_Z = "bpy.context.object.scale[2] = {val:4.2f}"

    DECLARE_CAMERAPATH_AS_VARIABLE = "camera_path = bpy.data.objects['CameraPath']"
    DECLARE_CAMERA_AS_VARIABLE = "camera = bpy.data.objects['Camera']"

    SET_CAMERAPATH_LOCATION = "camera_path.location = 0, 0, {val:4.2f}"
    SET_CAMERA_LOCATION = "camera.location = {val:4.2f}, 0, 0"

    SET_CAMERAPATH_SCALING = "camera_path.scale = {val:4.2f}, {val:4.2f}, {val:4.2f}"

    DELETE_ALL_ANIMATIONS = "bpy.ops.anim.channels_delete()"
