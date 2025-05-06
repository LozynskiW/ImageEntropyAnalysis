import sys
from abc import ABC

import numpy as np
from matplotlib import pyplot as plt

from blender3d_intergration.Interfaces import BasicBlenderPathCalculation
from blender3d_intergration.blender_python_commands import BlenderPythonCommands as bpy


class CirclePath(BasicBlenderPathCalculation, ABC):

    def __init__(self):
        self.__height = 0
        self.__radius = 10
        self.__center_x = 0
        self.__center_y = 0
        self.__center_z = 0
        self.__start_frame = 0
        self.__end_frame = 520
        self.__ang_freq = 1
        self.__velocity = 18  # m/s
        self.__fps = 30

    def set_path_parameters(self, height=None, radius=None, start_x=None, start_y=None, start_z=None,
                            start_frame=None, end_frame=None, ang_freq=None, fps=None):

        if height:
            self.__height = height

        if radius:
            self.__radius = radius

        if start_x:
            self.__center_x = start_x

        if start_y:
            self.__center_y = start_y

        if start_z:
            self.__center_z = start_z

        if start_frame:
            self.__start_frame = start_frame

        if end_frame:
            self.__end_frame = end_frame

        if ang_freq:
            self.__ang_freq = ang_freq

        if fps:
            self.__fps = fps

    def calculate_trajectory(self, camera_set=True):

        self.trajectory = []

        self.__end_frame = self.__get_end_frame()

        frame_num = self.__end_frame - self.__start_frame

        x, y, z = self.__get_trajectory_xyz_coordinates(frame_num=frame_num,
                                                        camera_set=camera_set)

        for frame in range(0, frame_num):
            self.trajectory.append({"x": x[frame], "y": y[frame], "z": z[frame]})

    def __get_end_frame(self):

        t = 2 * 3.14 * self.__radius / self.__velocity

        return int(t * self.__fps)

    def __get_trajectory_xyz_coordinates(self, frame_num, camera_set=False):

        x = []
        y = []
        z = []

        if not camera_set:

            for frame in range(0, frame_num):
                t = frame / self.__fps
                x.append(self.__radius * np.cos(self.__ang_freq * t))
                y.append(self.__radius * np.sin(self.__ang_freq * t))
                z.append(self.__center_z)
        else:

            step = 2 * self.__radius / frame_num

            for i in range(0, int(frame_num)):
                x.append(step * i)
                y.append(0)
                z.append(0)

        return x, y, z

    def plot(self):

        x = list(map(lambda i: i['x'], self.trajectory))
        y = list(map(lambda i: i['y'], self.trajectory))
        z = list(map(lambda i: i['z'], self.trajectory))

        fig, axs = plt.subplots(1, 3)
        axs[0].plot_2d(x, y)
        axs[1].plot_2d(x, z)
        axs[2].plot_2d(y, z)

        axs[0].set_title("X(Y)")
        axs[1].set_title("X(Z)")
        axs[2].set_title("Y(Z)")

        plt.grid()
        plt.show()

    def calculate_multiple_trajectories_and_save_to_script(self, path_to_files="/",
                                                           file_ext="txt",
                                                           camera_set=False,
                                                           radius=20,
                                                           height=40,
                                                           const_val='h',
                                                           end_val=50,
                                                           step=10):
        self.__height = height
        self.__radius = radius

        if const_val == 'h':
            start_val = self.__radius
        else:
            start_val = self.__height

        for trajectory_parameter in range(start_val, end_val + 1, step):

            if const_val == 'h':
                self.__radius = trajectory_parameter
            else:
                self.__height = trajectory_parameter

            file_name = 'h' + str(self.__height) + 'm_r' + str(self.__radius) + 'm'

            self.calculate_trajectory(camera_set=camera_set)

            full_file_path = path_to_files + '/' + file_name

            self.save_trajectory_as_blender_script(file_name=full_file_path, file_ext=file_ext, camera_set=camera_set)

    def save_trajectory_as_blender_script(self, file_name="trajectory", file_ext="txt", camera_set=False):

        if type(self.__end_frame) is float:
            raise ValueError("self.end_frame is float, should be int")

        if len(self.trajectory) != self.__end_frame:
            raise ValueError('len(self.trajectory)=', len(self.trajectory), " self.__end_frame=", int(self.__end_frame),
                             "\nLength of trajectory is not equal to number of keyframes")

        file = file_name + "." + file_ext
        f = open(file, 'w')
        sys.stdout = f
        keyframe = 0

        print(bpy.BPY_IMPORT)
        print(bpy.DESELECT_ALL)

        print(bpy.DECLARE_CAMERA_AS_VARIABLE)
        print(bpy.DECLARE_CAMERAPATH_AS_VARIABLE)
        print(bpy.SET_FRAME.format(val=0))
        print(bpy.SET_CAMERAPATH_LOCATION.format(val=self.__height))
        print(bpy.SET_CAMERAPATH_SCALING.format(val=self.__radius))
        print(bpy.SELECT_ALL)
        print(bpy.APPLY_LOCATION)
        print(bpy.APPLY_SCALING)
        print(bpy.DESELECT_ALL)

        if not camera_set:
            print(bpy.DESELECT_ALL)
            print(bpy.SELECT_CAMERA)
            print(bpy.ADD_CAMERA_TRACKING_TO_OBJECT)
            print(bpy.SET_CAMERA_TRACKING_TO_TARGET)
        print(bpy.SET_START_FRAME.format(val=self.__start_frame))
        print(bpy.SET_END_FRAME.format(val=self.__end_frame))
        print(bpy.DESELECT_ALL)

        for pos in self.trajectory:
            print(bpy.SET_FRAME.format(val=keyframe))

            print(bpy.SET_CAMERA_LOCATION.format(val=pos['x']))
            print(bpy.SET_CAMERAPATH_LOCATION.format(val=self.__height))
            print(bpy.SET_CAMERAPATH_SCALING.format(val=self.__radius))
            print(bpy.SELECT_ALL)
            print(bpy.APPLY_LOCATION)
            print(bpy.DESELECT_ALL)

            keyframe += 1

        sys.stdout = sys.stdout
