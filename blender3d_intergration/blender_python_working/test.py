import bpy

bpy.ops.object.select_all(action='DESELECT')

camera_path = bpy.data.objects["CameraPath"]
camera = bpy.data.objects["Camera"]

bpy.context.scene.frame_set(0)
camera.location = 0, 0, 0

bpy.ops.object.select_all(action='SELECT')
bpy.ops.anim.keyframe_insert_menu(type='Location')
bpy.ops.object.select_all(action='DESELECT')

bpy.context.scene.frame_set(50)
camera.location = 100, 0, 0

bpy.ops.object.select_all(action='SELECT')
bpy.ops.anim.keyframe_insert_menu(type='Location')
bpy.ops.object.select_all(action='DESELECT')

scene = bpy.context.scene
scene.render.image_settings.file_format='PNG'

bpy.ops.render.render(write_still=True, animation=True)