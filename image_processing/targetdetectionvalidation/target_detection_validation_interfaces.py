from app.data_collection_logs_analysis.ObjectGeoLoc import ObjectGeoLoc


class base:

    def __init__(self, verbose_mode=False, object_geo_loc_calculator=ObjectGeoLoc()):
        self.__verbose_mode = verbose_mode
        self.__object_geo_loc_calculator = object_geo_loc_calculator

    @property
    def verbose_mode(self):
        return self.__verbose_mode

    @verbose_mode.setter
    def verbose_mode(self, verbose_mode):
        self.__verbose_mode = verbose_mode

    @property
    def object_geo_loc_calculator(self):
        return self.__object_geo_loc_calculator

    @object_geo_loc_calculator.setter
    def object_geo_loc_calculator(self, object_geo_loc_calculator):
        self.__object_geo_loc_calculator = object_geo_loc_calculator

    def validate(self, target_coordinates, camera):
        raise NotImplementedError