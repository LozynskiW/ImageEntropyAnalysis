from abc import abstractmethod


class BasicBlenderPathCalculation:
    trajectory = []

    @abstractmethod
    def set_path_parameters(self):
        raise NotImplementedError

    def get_trajectory(self):
        return self.trajectory

    @abstractmethod
    def get_trajectory_as_blender_script(self):
        raise NotImplementedError

    @abstractmethod
    def calculate_trajectory(self):
        raise NotImplementedError

    @abstractmethod
    def plot(self):
        raise NotImplementedError
