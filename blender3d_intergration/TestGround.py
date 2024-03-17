from blender3d_intergration.Camera import CirclePath
from blender3d_intergration.Camera import TRAJECTORIES_PATH as PATH

blender_circle_trajectory_test = CirclePath()
blender_circle_trajectory_test.set_path_parameters(radius=10)
blender_circle_trajectory_test.calculate_trajectory()

for h in range(20, 101, 10):

    blender_circle_trajectory_test.calculate_multiple_trajectories(
        path_to_files=PATH,
        file_ext="txt",
        radius=20,
        height=h,
        camera_set=True,
        const_val='h',
        end_val=100,
        step=10
    )