from blender3d_intergration.blender_python.blender_commands_generator import blender_commands_from_trajectory
from blender3d_intergration.trajectories_api.models import FramesPerSecond, Coordinates
from blender3d_intergration.trajectories_api.trajectories_calculators.linear.calculators import SimpleLinearTrajectory
from blender3d_intergration.trajectories_api.trajectories_calculators.linear.models import \
    LinearTrajectoryMotionInitialParameters
from blender3d_intergration.config import linear_full_path

height_values_list = [20, 30, 40, 50, 60, 70, 80, 90, 100]

for height in height_values_list:
    start_point = Coordinates(x=10, y=0, z=height)
    end_point = Coordinates(x=100, y=0, z=height)

    linear_initial_params = LinearTrajectoryMotionInitialParameters(
        start_point=start_point,
        end_point=end_point,
        x_velocity_m_s=18,
        y_velocity_m_s=0,
        z_velocity_m_s=0
    )

    linear_trajectory = SimpleLinearTrajectory(linear_initial_params, FramesPerSecond.FPS_30)
    linear_trajectory.calculate_trajectory()

    blender_commands_from_trajectory(
        trajectory=linear_trajectory.get_trajectory(),
        path_to_files=linear_full_path,
        output_file_name=f"linear_z{height}m",
    )
