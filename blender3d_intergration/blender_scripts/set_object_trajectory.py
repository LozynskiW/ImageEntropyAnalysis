import os


def execute_commands_from_file(commands_file_path, file_name):
    filepath = f"{commands_file_path}/{file_name}"
    global_namespace = {"__file__": filepath, "__name__": "__main__"}

    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), global_namespace)
        print("...DONE")


# MAIN
trajectories_path = 'D:/python/ImageEntropyAnalysis/blender3d_intergration/trajectories_api/calculated_trajectories/manual'

object_for_trajectory = ["Camera"]

trajectories = os.listdir(trajectories_path)

for trajectory in trajectories:
    if "gps" in trajectory:
        continue

    print(f"Now processing: {trajectory}", end="")

    execute_commands_from_file(
        commands_file_path=trajectories_path,
        file_name=trajectory
    )
