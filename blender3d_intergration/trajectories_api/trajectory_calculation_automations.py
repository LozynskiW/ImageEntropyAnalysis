from blender3d_intergration.trajectories_api.circle_trajectory import \
    CircularMotionInitialParametersGenerator, SimpleCircleTrajectory
from blender3d_intergration.trajectories_api.models import FramesPerSecond, \
    CircularTrajectoryMotionInitialParameters


def circular_trajectories_constant_height(
        initial_motion_parameters: CircularTrajectoryMotionInitialParameters,
        fps: FramesPerSecond,
        radius_values_list: list[int]
) -> list[SimpleCircleTrajectory]:

    initial_params_list = (CircularMotionInitialParametersGenerator.changing_radius(
        center_point=initial_motion_parameters.trajectory_center_point,
        linear_velocity_m_s=initial_motion_parameters.linear_velocity_m_s,
        angular_displacement_degrees=initial_motion_parameters.angular_displacement_degrees,
        radius_m_list=radius_values_list
    ))

    trajectories_list = []

    for initial_param in initial_params_list:
        t = SimpleCircleTrajectory(initial_param, fps)
        t.calculate_trajectory()
        trajectories_list.append(t)

    return trajectories_list
