from enum import StrEnum


class BlenderPythonCommands(StrEnum):
    BPY_IMPORT = "import bpy"
    SELECT_ALL = "bpy.ops.object.select_all(action='SELECT')"
    DESELECT_ALL = "bpy.ops.object.select_all(action='DESELECT')"
    SELECT_CAMERA = 'bpy.data.objects["Camera"].select_set(True)'
    SELECT_LIGHT_SOURCE = 'bpy.data.objects["light_source"].select_set(True)'

    ADD_TRACk_TO_CONSTRAINT_FOR_SELECTED_OBJECT = "bpy.ops.object.constraint_add(type='TRACK_TO')"
    SET_TRACK_TO_CONSTRAINT_TO_TARGET_FOR_SELECTED_OBJECT = 'bpy.context.object.constraints["Track To"].target = bpy.data.objects["Target"]'
    DELETE_TRACK_TO_CONSTRAINT_TO_TARGET_FOR_SELECTED_OBJECT = 'bpy.ops.constraint.delete(constraint="Track To", owner="OBJECT")'
    SET_TRACK_TO_CONSTRAINT_UP_AXIS_Y_FOR_SELECTED_OBJECT = 'bpy.context.object.constraints["Track To"].up_axis = "UP_Y"'
    SET_TRACK_TO_CONSTRAINT_UP_AXIS_Z_FOR_SELECTED_OBJECT = 'bpy.context.object.constraints["Track To"].up_axis = "UP_Z"'
    SET_TRACK_TO_CONSTRAINT_TRACK_AXIS_TRACK_NEGATIVE_Z_FOR_SELECTED_OBJECT = 'bpy.context.object.constraints["Track To"].track_axis = "TRACK_NEGATIVE_Z"'

    ADD_DUMPED_TRACK_FOR_SELECTED_OBJECT = 'bpy.ops.object.constraint_add(type="DAMPED_TRACK")'
    SET_DUMPED_TRACK_FOR_SELECTED_OBJECT = 'bpy.context.object.constraints["Damped Track"].target = bpy.data.objects["Target"]'
    DELETE_DUMPED_TRACK_FOR_SELECTED_OBJECT = 'bpy.ops.constraint.delete(constraint="Damped Track", owner="OBJECT")'
    SET_DUMPED_TRACK_CONSTRAINT_TRACK_AXIS_TRACK_NEGATIVE_Z_FOR_SELECTED_OBJECT = 'bpy.context.object.constraints["Damped Track"].track_axis = "TRACK_NEGATIVE_Z"'

    ADD_COPY_LOCATION_CONSTRAINT_FOR_SELECTED_OBJECT = "bpy.ops.object.constraint_add(type='COPY_LOCATION')"
    SET_COPY_LOCATION_TO_CAMERA_FOR_SELECTED_OBJECT = 'bpy.context.object.constraints["Copy Location"].target = bpy.data.objects["Camera"]'
    DELETE_COPY_LOCATION_TO_CAMERA_FOR_SELECTED_OBJECT = 'bpy.ops.constraint.delete(constraint="Copy Location.001", owner="OBJECT")'

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

    SET_CAMERAPATH_LOCATION_Z = "camera_path.location = 0, 0, {val:4.2f}"
    SET_CAMERAPATH_LOCATION_X_Y_Z = "camera_path.location = {val:4.2f}, {val:4.2f}, {val:4.2f}"
    SET_CAMERA_LOCATION = "camera.location = {val:4.2f}, 0, 0"
    SET_CAMERA_LOCATION_X_Y_Z = "camera.location = {x:4.2f}, {y:4.2f}, {z:4.2f}"

    SET_CAMERAPATH_SCALING_X_Y_Z = "camera_path.scale = {val:4.2f}, {val:4.2f}, {val:4.2f}"

    DELETE_ALL_ANIMATIONS = "bpy.ops.anim.channels_delete()"
