from enum import Enum

import bpy, os

trajectories_full_path = 'D:/python/ImageEntropyAnalysis/blender3d_intergration/object_trajectory_calculation/calculated_trajectories/test'

ANIMATIONS_PATH = 'D:/artykuly/wat_2/test_animations/new'

# objects
DEER = bpy.data.objects['deer']
WILD_BOAR = bpy.data.objects['wild_boar']
RABBIT = bpy.data.objects['Armature']
SPHERE = bpy.data.objects['sphere']


def render_test_animations_for_object_for_all_trajectories(object, trajectories_path, output_path):
    if object == 'deer':
        object_class = DEER
    elif object == 'wild_boar':
        object_class = WILD_BOAR
    elif object == 'rabbit':
        object_class = RABBIT
    elif object == 'sphere':
        object_class = SPHERE
    else:
        raise ValueError("No such class of object possible")

    output_path = f"{output_path}/{object}/"

    bpy.ops.object.select_all(action='SELECT')
    bpy.context.object.location[2] = -10
    bpy.ops.object.select_all(action='DESELECT')

    # if object == 'deer':
    #     object_class.location = 0, 0, 1.13
    # elif object == 'wild_boar':
    #     object_class.location = 0, 0, 0.74
    # elif object == 'rabbit':
    #     object_class.location = 0, 0, 0

    render_test_animations_for_scene_for_all_trajectories(
        trajectories_path=trajectories_path,
        output_path=output_path
    )


def render_test_animations_for_scene_for_all_trajectories(trajectories_path, output_path):
    trajectories = os.listdir(trajectories_path)
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'

    for trajectory in trajectories:
        print("Now processing: ", trajectory, end="")
        create_renders_for_given_trajectory_path(trajectory_path=trajectories_path, file_name=trajectory,
                                                 output_path=output_path)


def create_renders_for_given_trajectory_path(trajectory_path, file_name, output_path):
    folder_name = file_name.split('.')[0]
    filepath = trajectory_path + '/' + file_name
    global_namespace = {"__file__": filepath, "__name__": "__main__"}

    # output_path = path + '/' + trajectory.split('.')[0] + '/'

    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), global_namespace)
        print("...DONE")

    scene = bpy.context.scene
    scene.render.filepath = output_path + '/' + folder_name + '/'
    bpy.ops.render.render(write_still=True, animation=True)


# MAIN
animals_objects_list = [DEER, WILD_BOAR, RABBIT]
geometrics_objects_list = ["sphere"]
print('RENDER START')

for obj_class in geometrics_objects_list:
    render_test_animations_for_object_for_all_trajectories(
        object=obj_class,
        trajectories_path=trajectories_full_path,
        output_path=ANIMATIONS_PATH,
    )

print('RENDER END')
