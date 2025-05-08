import os
import sys

from blender3d_intergration.blender_python_commands import BlenderPythonCommands as bpy

from blender3d_intergration.enums import FileExtensions
from blender3d_intergration.object_trajectory_calculation.models import Trajectory, Coordinates


class TrajectoryToBlenderCommands:

    @staticmethod
    def to_bpy(trajectory: Trajectory,
               path_to_files: str = os.path.dirname(__file__),
               output_file_name: str = 'trajectory',
               output_file_ext: FileExtensions = FileExtensions.TXT,
               camera_name: str = "Camera",
               camera_path_name: str = "CameraPath"):

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
        print(bpy.DECLARE_CAMERAPATH_AS_VARIABLE)

        print(bpy.DESELECT_ALL)
        print(bpy.SELECT_CAMERA)
        print(bpy.ADD_CAMERA_TRACKING_TO_OBJECT)
        print(bpy.SET_CAMERA_TRACKING_TO_TARGET)
        print(bpy.SET_START_FRAME.format(val=0))
        print(bpy.SET_END_FRAME.format(val=trajectory.get_last_frame()))
        print(bpy.DESELECT_ALL)

    @staticmethod
    def __apply_location_for_camera(coordinates: Coordinates):
        print(bpy.SET_FRAME.format(val=coordinates.frame))

        print(bpy.SET_CAMERA_LOCATION_X_Y_Z.format(x=coordinates.x, y=coordinates.y, z=coordinates.z))
        print(bpy.SELECT_ALL)
        print(bpy.APPLY_LOCATION)
        print(bpy.DESELECT_ALL)