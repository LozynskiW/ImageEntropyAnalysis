import bpy, os


# objects

DEER = bpy.data.objects['deer']
WILD_BOAR = bpy.data.objects['wild_boar']
RABBIT = bpy.data.objects['Armature']
SPHERE = bpy.data.objects['sphere']


def render_test_animations_for_object_for_all_trajectories(object, trajectories_path, output_path):

    global_path = {"__file__": trajectories_path, "__name__": "__main__"}
    output_path = f"{output_path}/{object}/"

    print(global_path)

    trajectories = os.listdir(trajectories_path)
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'

    for trajectory in trajectories:
        print(f"Now processing: {trajectory}", end="")

        execute_commands_from_file(
            commands_file_path=trajectories_path,
            file_name=trajectory,
            output_path=output_path)


def execute_commands_from_file(commands_file_path, file_name, output_path):
    folder_name = file_name.split('.')[0]
    filepath = f"{commands_file_path}/{file_name}"
    global_namespace = {"__file__": filepath, "__name__": "__main__"}

    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), global_namespace)
        print("...DONE")

    scene = bpy.context.scene
    scene.render.filepath = f"{output_path}/{folder_name}/"
    bpy.ops.render.render(write_still=True, animation=True)


# MAIN
TRAJECTORIES_PATH = 'D:/python/ImageEntropyAnalysis/blender3d_intergration/trajectories_api/calculated_trajectories/manual'

ANIMATIONS_PATH = 'D:/artykuly/wat_2/test_animations/manual'

animals_objects_list = [DEER, WILD_BOAR, RABBIT]
geometrics_objects_list = ["sphere"]
print('RENDER START')

for obj_class in geometrics_objects_list:
    render_test_animations_for_object_for_all_trajectories(
        object=obj_class,
        trajectories_path=TRAJECTORIES_PATH,
        output_path=ANIMATIONS_PATH,
    )

print('RENDER END')
