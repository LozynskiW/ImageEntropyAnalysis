from enum import StrEnum


class BlenderPythonCommands(StrEnum):
    BPY_IMPORT = "import bpy"
    SELECT_ALL = "bpy.ops.object.select_all(action='SELECT')"
    DESELECT_ALL = "bpy.ops.object.select_all(action='DESELECT')"
    SELECT_OBJECT = 'bpy.data.objects["{obj_name:s}"].select_set(True)'
    SELECT_LIGHT_SOURCE = 'bpy.data.objects["light_source"].select_set(True)'

    DISABLE_RENDER_FOR_SELECTED_OBJ = 'bpy.context.object.hide_render = True'
    ENABLE_RENDER_FOR_SELECTED_OBJ = 'bpy.context.object.hide_render = False'
    DISABLE_RENDER_BY_NAME = 'bpy.data.objects[name:%s].hide_render = True'
    ENABLE_RENDER_BY_NAME = 'bpy.data.objects[name:%s].hide_render = False'

    ITERATE_OVER_ALL_OBJECTS = 'for o in bpy.data.objects:'
    DISABLE_RENDER_BY_NAME_OF_ITERATED_OBJ = '\tbpy.data.objects[o.name].hide_render = True'

    ADD_TRACK_TO_CONSTRAINT_FOR_SELECTED_OBJECT = "bpy.ops.object.constraint_add(type='TRACK_TO')"
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

    SET_OBJECT_LOCATION_X_Y_Z = 'bpy.data.objects["{obj_name:s}"].location = {x:4.2f}, {y:4.2f}, {z:4.2f}'

    DELETE_ALL_ANIMATIONS = "bpy.ops.anim.channels_delete()"

    SELECT_MATERIAL_AT_INDEX = "bpy.context.object.active_material_index = {val:d}"
    TOGGLE_EDIT_MODE = "bpy.ops.object.editmode_toggle()"
    SELECT_ALL_OBJECT_FACES = "bpy.ops.mesh.select_all(action='SELECT')"

    SET_WORLD_BACKGROUND_COLOR_RGB = 'bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = ({r:1.6f}, {g:1.6f}, {b:1.6f}, 1)'
