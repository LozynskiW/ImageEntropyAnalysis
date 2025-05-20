import os
import sys

from blender3d_intergration.blender_python_working.blender_python_commands import BlenderPythonCommands as bpy

from blender3d_intergration.enums import FileExtensions
from blender3d_intergration.trajectories_api.models import Trajectory, Coordinates


class TrajectoryToBlenderCommands:

    @staticmethod
    def save_to_file(trajectory: Trajectory,
                     path_to_files: str = os.path.dirname(__file__),
                     output_file_name: str = 'trajectory',
                     output_file_ext: FileExtensions = FileExtensions.TXT) -> None:

        output_file = path_to_files + '/' + output_file_name + "." + output_file_ext
        try:
            file = open(output_file, 'w')
        except FileNotFoundError:
            file = open(output_file, 'x')

        sys.stdout = file

        TrajectoryToBlenderCommands.__set_scene(trajectory)

        for coordinates in trajectory.get_coordinates():
            TrajectoryToBlenderCommands.__apply_location_for_camera(coordinates)

        sys.stdout = sys.stdout
        file.close()

    @staticmethod
    def __set_scene(trajectory: Trajectory):
        print(bpy.BPY_IMPORT)
        print(bpy.DESELECT_ALL)
        print(bpy.DECLARE_CAMERA_AS_VARIABLE)
        print(bpy.DESELECT_ALL)

        print(bpy.SELECT_CAMERA)

        print(bpy.DELETE_TRACK_TO_CONSTRAINT_TO_TARGET_FOR_SELECTED_OBJECT)
        print(bpy.ADD_TRACk_TO_CONSTRAINT_FOR_SELECTED_OBJECT)
        print(bpy.SET_TRACK_TO_CONSTRAINT_TO_TARGET_FOR_SELECTED_OBJECT)
        print(bpy.SET_TRACK_TO_CONSTRAINT_UP_AXIS_Y_FOR_SELECTED_OBJECT)
        print(bpy.SET_TRACK_TO_CONSTRAINT_TRACK_AXIS_TRACK_NEGATIVE_Z_FOR_SELECTED_OBJECT)
        print(bpy.DESELECT_ALL)

        print(bpy.SELECT_LIGHT_SOURCE)

        print(bpy.DELETE_TRACK_TO_CONSTRAINT_TO_TARGET_FOR_SELECTED_OBJECT)
        print(bpy.ADD_DUMPED_TRACK_FOR_SELECTED_OBJECT)
        print(bpy.SET_DUMPED_TRACK_FOR_SELECTED_OBJECT)
        print(bpy.SET_DUMPED_TRACK_CONSTRAINT_TRACK_AXIS_TRACK_NEGATIVE_Z_FOR_SELECTED_OBJECT)

        print(bpy.DELETE_COPY_LOCATION_TO_CAMERA_FOR_SELECTED_OBJECT)
        print(bpy.ADD_COPY_LOCATION_CONSTRAINT_FOR_SELECTED_OBJECT)
        print(bpy.SET_COPY_LOCATION_TO_CAMERA_FOR_SELECTED_OBJECT)
        print(bpy.DESELECT_ALL)

        print(bpy.SET_START_FRAME.format(val=0))
        print(bpy.SET_END_FRAME.format(val=trajectory.get_last_frame()))

    @staticmethod
    def __apply_location_for_camera(coordinates: Coordinates):
        print(bpy.SET_FRAME.format(val=coordinates.frame))

        print(bpy.SET_CAMERA_LOCATION_X_Y_Z.format(x=coordinates.x, y=coordinates.y, z=coordinates.z))
        print(bpy.SELECT_ALL)
        print(bpy.APPLY_LOCATION)
        print(bpy.DESELECT_ALL)