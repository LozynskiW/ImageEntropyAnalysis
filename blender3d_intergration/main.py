import os

from blender3d_intergration.object_trajectory_calculation.circle_trajectory import SimpleCircleTrajectory
from blender3d_intergration.object_trajectory_calculation.models import Coordinates, \
    CircularTrajectoryMotionInitialParameters, FramesPerSecond

trajectories_path = './object_trajectory_calculation/calculated_trajectories/new'
script_dir = os.path.dirname(__file__)
full_path = os.path.join(script_dir, trajectories_path)

trajectory_center_point = Coordinates(0, 0, 30, 0, 0)

initial_params = CircularTrajectoryMotionInitialParameters(
    trajectory_center_point=trajectory_center_point,
    linear_velocity_m_s=18,
    angular_displacement_degrees=360,
    radius_m=20
)

circular_trajectory = SimpleCircleTrajectory(initial_params, FramesPerSecond.FPS_30)
circular_trajectory.calculate_trajectory()
circular_trajectory.plot()
