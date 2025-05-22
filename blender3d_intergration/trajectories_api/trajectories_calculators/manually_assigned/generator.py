from blender3d_intergration.blender_python.blender_commands_generator import blender_commands_from_trajectory, gps_data_from_trajectory
from blender3d_intergration.trajectories_api.models import CoordinatesInTime, Coordinates, FramesPerSecond
from blender3d_intergration.trajectories_api.trajectories_calculators.manually_assigned.calculators import \
    ManuallyAssignedCoordinatesTrajectory

from blender3d_intergration.config import manual_full_path

const_y = 0
x_values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
z_values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

frame: int = 1
coordinates_list = []
for x in x_values:

    for z in z_values:
        coordinates_list.append(
            CoordinatesInTime(Coordinates(x, const_y, z), frame, frame))
        frame += 1

manually_defined_trajectory = ManuallyAssignedCoordinatesTrajectory(coordinates_list, FramesPerSecond.FPS_30)
manually_defined_trajectory.calculate_trajectory()

blender_commands_from_trajectory(
    trajectory=manually_defined_trajectory.get_trajectory(),
    path_to_files=manual_full_path,
    output_file_name="manual",
)

gps_data_from_trajectory(
    trajectory=manually_defined_trajectory.get_trajectory(),
    path_to_files=manual_full_path,
    output_file_name="manual_gps",
)
