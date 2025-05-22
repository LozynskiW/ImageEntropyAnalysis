from blender3d_intergration.blender_python.blender_commands_generator import TrajectoryToBlenderCommands
from blender3d_intergration.trajectories_api.models import CoordinatesInTime, FramesPerSecond, Coordinates
from blender3d_intergration.trajectories_api.trajectories_calculators.circular.calculators import SimpleCircleTrajectory
from blender3d_intergration.trajectories_api.trajectories_calculators.circular.models import \
    CircularTrajectoryMotionInitialParameters
from blender3d_intergration.config import circular_full_path

radius_values_list = [20, 30, 40, 50, 60, 70, 80, 90, 100]
height_values_list = [30, 40, 50, 60, 70, 80, 90, 100]

linear_velocity_m_s = 18

for height in height_values_list:

    trajectory_center_point = Coordinates(0, 0, height)

    for radius in radius_values_list:

        initial_params = CircularTrajectoryMotionInitialParameters(
            trajectory_center_point=trajectory_center_point,
            linear_velocity_m_s=linear_velocity_m_s,
            angular_displacement_degrees=360,
            radius_m=radius
        )

        trajectory_for_radius_and_height = SimpleCircleTrajectory(
            fps=FramesPerSecond.FPS_30,
            initial_motion_parameters=initial_params
        )

        trajectory_for_radius_and_height.calculate_trajectory()

        TrajectoryToBlenderCommands.save_to_file(
            trajectory=trajectory_for_radius_and_height.get_trajectory(),
            path_to_files=circular_full_path,
            output_file_name=f"h{height}m_r{radius}m",
        )