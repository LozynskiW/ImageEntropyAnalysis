from image_processing.definitions import ConfigurableImageSegmentationSystem


class ApplicationManagement:

    def __init__(self,
                 image_segmentation_system: ConfigurableImageSegmentationSystem):

        # Dependencies
        self.__data_base = Mongo()
        self.__local_storage = on_disk()
        self.__image_segmentation_system = image_segmentation_system
        self.__data_unification_for_plotting = DataUnificationForPlotting()

        # Local storage and database coordinates for data extraction
        self.__object = None
        self.__dataset = None