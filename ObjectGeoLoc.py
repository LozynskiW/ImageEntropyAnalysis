
class ObjectGeoLoc:
    def __init__(self):
        self.__img = None

        self.__barometric_height = 0
        self.__gps_height = 0
        self.__pitch = 0
        self.__roll = 0
        self.__yaw = 0

        self.__dist_per_pixel_width = 0
        self.__dist_per_pixel_height = 0

        self.__camera_fov = 0
        self.__angle = 0

        self.__camera_zenmuse = Camera(fov_vertically_in_degree=42.44, fov_horizontally_in_degree=57.12)
        self.__camera_ktx = Camera(fov_vertically_in_degree=22, fov_horizontally_in_degree=28)
        self.__selected_camera = self.__camera_zenmuse

    def setup(self, camera):
        self.__select_camera(camera)

    def __select_camera(self, camera):
        if camera == 'zenmuse' or camera == 'antrax':
            self.__selected_camera = self.__camera_zenmuse
        if camera == 'ktx' or camera == 'new':
            self.__selected_camera = self.__camera_ktx

    def get_camera_horizontal_fov(self):
        return self.__selected_camera.get_fov_horizontal_deg()

    def get_camera_vertical_fov(self):
        return self.__selected_camera.get_fov_vertical_deg()

    def add_img(self, img, log):
        self.__set_img(img)
        self.__set_geo_loc_data(log)

    def __set_geo_loc_data(self, log):
        if log is not None:
            self.__longitude = log["longitude"]
            self.__latitude = log["latitude"]
            self.__gps_height = log["gps_height"]
            self.__barometric_height = log["barometric_height"]
            self.__pitch = log["pitch"]
            self.__roll = log["roll"]
            self.__yaw = log["yaw"]
            self.__gps_speed = log["gps_speed"]
            self.__gps_course = log["gps_course"]

    def __set_img(self, img):
        self.__img = img

    def calculate_angle_from_obj_to_camera_center(self):
        img_width = len(self.__img[0])
        img_height = len(self.__img)

        center_y = int(img_height / 2)
        center_x = int(img_width / 2)

        mean_x = 0
        mean_y = 0

        divisor = 0

        for y in range(0, img_height):
            for x in range(0, img_width):
                if self.__img[y][x] > 0:
                    mean_x += self.__img[y][x] * x
                    mean_y += self.__img[y][x] * y
                    divisor += self.__img[y][x]

        if divisor == 0:
            return None, None

        mean_x = int(mean_x / divisor)
        mean_y = int(mean_y / divisor)

        distance_x = abs(center_x - mean_x)
        distance_y = abs(center_y - mean_y)

        horizontal_angle_per_pixel = self.__selected_camera.get_fov_horizontal_deg() / img_width
        vertical_angle_per_pixel = self.__selected_camera.get_fov_vertical_deg() / img_height

        horizontal_angle_dist_from_center = distance_x * horizontal_angle_per_pixel
        vertical_angle_dist_from_center = distance_y * vertical_angle_per_pixel

        return horizontal_angle_dist_from_center, vertical_angle_dist_from_center


class Camera:
    def __init__(self, fov_vertically_in_degree, fov_horizontally_in_degree):
        self.__fov_vertically_in_degree = fov_vertically_in_degree
        self.__fov_horizontally_in_degree = fov_horizontally_in_degree

    def get_fov_horizontal_deg(self):
        return self.__fov_horizontally_in_degree

    def get_fov_vertical_deg(self):
        return self.__fov_vertically_in_degree
