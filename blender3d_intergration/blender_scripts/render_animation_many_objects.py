import bpy


def hide_all_objects_except(obj_name):
    for o in bpy.data.objects:
        bpy.data.objects[o.name].hide_render = True

    bpy.data.objects[obj_name].hide_render = False


ANIMATIONS_PATH = 'D:/artykuly/wat_2/test_animations/manual'

geometrics_objects_list = ["cylinder", "cube", "cone", "sphere"]
dataset_name = 'white_noise'

scene = bpy.context.scene
scene.render.image_settings.file_format = 'PNG'

print('RENDER START')
for obj_class in geometrics_objects_list:

    scene.render.filepath = f"{ANIMATIONS_PATH}/{obj_class}/{dataset_name}/"
    hide_all_objects_except(obj_class)
    bpy.ops.render.render(write_still=True, animation=True)

print('RENDER END')
