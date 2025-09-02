import copy

from blender3d_intergration.blender_python.blender_commands_generator import blender_commands_from_trajectory, \
    gps_data_from_trajectory
from blender3d_intergration.enums import FileExtensions
from blender3d_intergration.trajectories_api.models import CoordinatesInTime, Coordinates, FramesPerSecond
from blender3d_intergration.trajectories_api.trajectories_calculators.manually_assigned.calculators import \
    ManuallyAssignedCoordinatesTrajectory

from blender3d_intergration.config import manual_full_path

const_y = 0
x_values = [10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200]
z_values = copy.deepcopy(x_values)


def _generate_coordinates_in_time(
        x_values: list[int] | int,
        y_values: list[int] | int,
        z_values: list[int] | int) -> list[CoordinatesInTime]:
    frame: int = 1
    coordinates_list = []
    for x in x_values:
        for z in z_values:
            coordinates_list.append(
                CoordinatesInTime(Coordinates(x, const_y, z), frame, frame))
            frame += 1
    return coordinates_list


manually_defined_trajectory = ManuallyAssignedCoordinatesTrajectory(
    coordinates_in_time=_generate_coordinates_in_time(x_values, const_y, z_values),
    fps=FramesPerSecond.FPS_30
)
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
    output_file_ext=FileExtensions.JSON
)
