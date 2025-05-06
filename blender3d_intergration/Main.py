import os

from blender3d_intergration.enums import FlightParameters, FileExtensions
from blender3d_intergration.object_trajectory_calculation.Camera import CirclePath

trajectories_path = './object_trajectory_calculation/calculated_trajectories'
script_dir = os.path.dirname(__file__)
full_path = os.path.join(script_dir, trajectories_path)

blender_circle_trajectory_test = CirclePath()
blender_circle_trajectory_test.set_path_parameters(radius=10)
blender_circle_trajectory_test.calculate_trajectory()

for h in range(20, 101, 10):

    blender_circle_trajectory_test.calculate_multiple_trajectories_and_save_to_script(
        path_to_files=full_path,
        file_ext=FileExtensions.TXT,
        radius=20,
        height=h,
        camera_set=True,
        const_val=FlightParameters.HEIGHT,
        end_val=100,
        step=10
    )