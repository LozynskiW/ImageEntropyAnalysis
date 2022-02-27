import sys

from Interfaces import BasicBlenderPathCalculation
import numpy as np
import blender_python_commands as bpy
from matplotlib import pyplot as plt


class CirclePath(BasicBlenderPathCalculation):

    def __init__(self):
        self.__height = 0
        self.__radius = 10
        self.__center_x = 0
        self.__center_y = 0
        self.__center_z = 0
        self.__start_frame = 0
        self.__end_frame = 100
        self.__ang_freq = 1
        self.__fps = 24

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

    def calculate_trajectory(self):

        self.trajectory.append({"x": self.__radius, "y": self.__center_y, "z": self.__center_z})

        for frame in range(self.__start_frame, self.__end_frame):
            t = frame / self.__fps

            x = self.__radius * np.cos(self.__ang_freq * t)
            y = self.__radius * np.sin(self.__ang_freq * t)
            z = self.__center_z

            self.trajectory.append({"x": x, "y": y, "z": z})

    def plot(self):

        x = list(map(lambda i: i['x'], self.trajectory))
        y = list(map(lambda i: i['y'], self.trajectory))
        z = list(map(lambda i: i['z'], self.trajectory))

        fig, axs = plt.subplots(1, 3)
        axs[0].plot(x, y)
        axs[1].plot(x, z)
        axs[2].plot(y, z)

        axs[0].set_title("X(Y)")
        axs[1].set_title("X(Z)")
        axs[2].set_title("Y(Z)")

        plt.grid()
        plt.show()

    def get_trajectory_as_blender_script(self):

        f = open('trajectory.txt', 'w')
        sys.stdout = f
        keyframe = 0

        print(bpy.BPY_IMPORT)
        print(bpy.DESELECT_ALL)
        print(bpy.SELECT_CAMERA)
        print(bpy.ADD_CAMERA_TRACKING_TO_OBJECT)
        print(bpy.SET_CAMERA_TRACKING_TO_TARGET)
        print(bpy.SET_START_KEYFRAME.format(val=self.__start_frame))
        print(bpy.SET_END_KEYFRAME.format(val=self.__end_frame))
        print(bpy.DESELECT_ALL)
        print(bpy.SELECT_CAMERA)

        for pos in self.trajectory:

            x_position_script = bpy.ABSOLUTE_POSITION_X.format(val=pos['x'])
            y_position_script = bpy.ABSOLUTE_POSITION_Y.format(val=pos['y'])
            z_position_script = bpy.ABSOLUTE_POSITION_Z.format(val=pos['z'])

            print(bpy.SET_KEYFRAME.format(val=keyframe))

            print(x_position_script)
            print(y_position_script)
            print(z_position_script)
            print(bpy.APPLY_LOCATION)

            keyframe += 1

        sys.stdout = sys.stdout
