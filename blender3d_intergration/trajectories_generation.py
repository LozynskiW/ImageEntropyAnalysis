import os

from blender3d_intergration.blender_python_working.blender_commands_generator import TrajectoryToBlenderCommands
from blender3d_intergration.trajectories_api.linear_trajectory import SimpleLinearTrajectory
from blender3d_intergration.trajectories_api.models import CircularTrajectoryMotionInitialParameters, \
    FramesPerSecond, Coordinates, LinearTrajectoryMotionInitialParameters
from blender3d_intergration.trajectories_api.trajectory_calculation_automations import \
    circular_trajectories_constant_height

radius_values_list = [20, 30, 40, 50, 60, 70, 80, 90, 100]
height_values_list = [30, 40, 50, 60, 70, 80, 90, 100]

linear_velocity_m_s = 18

trajectories_path = 'trajectories_api/calculated_trajectories/new'
linear_trajectories_path = 'trajectories_api/calculated_trajectories/linear'
script_dir = os.path.dirname(__file__)
full_path = os.path.join(script_dir, trajectories_path)
linear_full_path = os.path.join(script_dir, linear_trajectories_path)

# for height in height_values_list:
#
#     trajectory_center_point = Coordinates(0, 0, height, 0, 0)
#
#     initial_params = CircularTrajectoryMotionInitialParameters(
#         trajectory_center_point=trajectory_center_point,
#         linear_velocity_m_s=linear_velocity_m_s,
#         angular_displacement_degrees=360,
#         radius_m=0
#     )
#
#     trajectories_for_constant_height_changing_radius = circular_trajectories_constant_height(
#         fps=FramesPerSecond.FPS_30,
#         initial_motion_parameters=initial_params,
#         radius_values_list=radius_values_list
#     )
#
#     for t in trajectories_for_constant_height_changing_radius:
#         radius = t.get_initial_motion_parameters().radius_m
#         command_printer = TrajectoryToBlenderCommands.to_bpy(
#             trajectory=t.get_trajectory(),
#             path_to_files=full_path,
#             output_file_name=f"h{height}m_r{radius}m",
#         )

for height in height_values_list:
    start_point = Coordinates(x=10, y=0, z=height, frame=0, time_s=0),
    end_point = Coordinates(x=100, y=0, z=height, frame=0, time_s=0),

    linear_initial_params = LinearTrajectoryMotionInitialParameters(
        start_point=Coordinates(x=10, y=0, z=30, frame=0, time_s=0),
        end_point=Coordinates(x=100, y=0, z=30, frame=0, time_s=0),
        x_velocity_m_s=18,
        y_velocity_m_s=0,
        z_velocity_m_s=0
    )

    linear_trajectory = SimpleLinearTrajectory(linear_initial_params, FramesPerSecond.FPS_30)
    linear_trajectory.calculate_trajectory()

    command_printer = TrajectoryToBlenderCommands.to_bpy(
        trajectory=linear_trajectory.get_trajectory(),
        path_to_files=linear_full_path,
        output_file_name=f"linear_z{height}m",
    )
