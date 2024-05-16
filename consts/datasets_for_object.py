
class DEER:

    @staticmethod
    def dataset_name():
        return 'deer'

    @staticmethod
    def height_20m_set():
        return ["h20m_r20m", "h20m_r30m", "h20m_r40m", "h20m_r50m", "h20m_r60m", "h20m_r70m", "h20m_r80m", "h20m_r90m", 
                "h20m_r100m"]

    @staticmethod
    def height_30m_set():
        return ["h30m_r20m", "h30m_r30m", "h30m_r40m", "h30m_r50m", "h30m_r60m", "h30m_r70m", "h30m_r80m", "h30m_r90m",
                "h30m_r100m"]

    @staticmethod
    def height_40m_set():
        return ["h40m_r20m", "h40m_r30m", "h40m_r40m", "h40m_r50m", "h40m_r60m", "h40m_r70m", "h40m_r80m", "h40m_r90m",
                "h40m_r100m"]

    @staticmethod
    def height_50m_set():
        return ["h50m_r20m", "h50m_r30m", "h50m_r40m", "h50m_r50m", "h50m_r60m", "h50m_r70m", "h50m_r80m", "h50m_r90m",
                "h50m_r100m"]

    @staticmethod
    def height_60m_set():
        return ["h60m_r20m", "h60m_r30m", "h60m_r40m", "h60m_r50m", "h60m_r60m", "h60m_r70m", "h60m_r80m", "h60m_r90m",
                "h60m_r100m"]

    @staticmethod
    def height_70m_set():
        return ["h70m_r20m", "h70m_r30m", "h70m_r40m", "h70m_r50m", "h70m_r60m", "h70m_r70m", "h70m_r80m", "h70m_r90m",
                "h70m_r100m"]

    @staticmethod
    def height_80m_set():
        return ["h80m_r20m", "h80m_r30m", "h80m_r40m", "h80m_r50m", "h80m_r60m", "h80m_r70m", "h80m_r80m", "h80m_r90m",
                "h80m_r100m"]

    @staticmethod
    def height_90m_set():
        return ["h90m_r20m", "h90m_r30m", "h90m_r40m", "h90m_r50m", "h90m_r60m", "h90m_r70m", "h90m_r80m", "h90m_r90m",
                "h90m_r100m"]

    @staticmethod
    def height_100m_set():
        return ["h100m_r20m", "h100m_r30m", "h100m_r40m", "h100m_r50m", "h100m_r60m", "h100m_r70m", "h100m_r80m",
                "h100m_r90m", "h100m_r100m"]

    @staticmethod
    def all_datasets():
        return [*DEER.height_20m_set(),
                *DEER.height_30m_set(),
                *DEER.height_40m_set(),
                *DEER.height_50m_set(),
                *DEER.height_60m_set(),
                *DEER.height_70m_set(),
                *DEER.height_80m_set(),
                *DEER.height_90m_set(),
                *DEER.height_100m_set()]
