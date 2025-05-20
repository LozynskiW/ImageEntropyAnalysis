import os

radius_values_list = [20, 30, 40, 50, 60, 70, 80, 90, 100]
height_values_list = [30, 40, 50, 60, 70, 80, 90, 100]

linear_velocity_m_s = 18

circular_trajectories_path = 'trajectories_api/calculated_trajectories/circular'
linear_trajectories_path = 'trajectories_api/calculated_trajectories/linear/test'
script_dir = os.path.dirname(__file__)
circular_full_path = os.path.join(script_dir, circular_trajectories_path)
linear_full_path = os.path.join(script_dir, linear_trajectories_path)

