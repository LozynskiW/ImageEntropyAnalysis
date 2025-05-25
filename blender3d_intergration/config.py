import os

circular_trajectories_path = 'trajectories_api/calculated_trajectories/circular'
linear_trajectories_path = 'trajectories_api/calculated_trajectories/linear'
manual_trajectories_path = 'trajectories_api/calculated_trajectories/manual'

script_dir = os.path.dirname(__file__)

circular_full_path = os.path.join(script_dir, circular_trajectories_path)
linear_full_path = os.path.join(script_dir, linear_trajectories_path)
manual_full_path = os.path.join(script_dir, manual_trajectories_path)
