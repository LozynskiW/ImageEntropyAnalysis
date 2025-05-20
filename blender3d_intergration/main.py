import os

import numpy as np

from blender3d_intergration.trajectories_api.trajectories_calculators.circular.calculators import SimpleCircleTrajectory
from blender3d_intergration.trajectories_api.trajectories_calculators.linear.calculators import SimpleLinearTrajectory
from blender3d_intergration.trajectories_api.models import CoordinatesInTime, FramesPerSecond

trajectories_path = 'trajectories_api/calculated_trajectories/new'
script_dir = os.path.dirname(__file__)
full_path = os.path.join(script_dir, trajectories_path)

trajectory_center_point = CoordinatesInTime(0, 0, 30, 0, 0)

initial_params = CircularTrajectoryMotionInitialParameters(
    trajectory_center_point=trajectory_center_point,
    linear_velocity_m_s=18,
    angular_displacement_degrees=360,
    radius_m=20
)

circular_trajectory = SimpleCircleTrajectory(initial_params, FramesPerSecond.FPS_30)
circular_trajectory.calculate_trajectory()
circular_trajectory.plot()

linear_initial_params = LinearTrajectoryMotionInitialParameters(
    start_point=CoordinatesInTime(x=10, y=0, z=30, frame=0, time_s=0),
    end_point=CoordinatesInTime(x=100, y=0, z=30, frame=0, time_s=0),
    x_velocity_m_s=18*np.sqrt(2),
    y_velocity_m_s=0,
    z_velocity_m_s=0
)

linear_trajectory = SimpleLinearTrajectory(linear_initial_params, FramesPerSecond.FPS_30)
linear_trajectory.calculate_trajectory()
linear_trajectory.plot()

