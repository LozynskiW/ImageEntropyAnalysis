from data_visualisation.models import PlotColor, PlotMarker

ALL_OBJECTS_LIST = ['sphere', 'cube', 'cone', 'cylinder']
ALL_DATASETS_LIST = ['white_only', 'gradient', 'white_noise']

ALTERING_BACKGROUND_LIGHT_DATASETS = [
    'white_noise',
    'white_noise_background_636363FF',
    'white_noise_background_A5A5A5FF',
    'white_noise_background_CFCFCFFF',
    'white_noise_background_F0F0F0FF'
]
ALL_Z_VALUES = [10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 240, 280, 320, 360, 400, 450, 500]

objects = {
    'cube': {'color': PlotColor.BLUE, 'marker': PlotMarker.PLUS},
    'cone': {'color': PlotColor.GREEN, 'marker': PlotMarker.STAR},
    'sphere': {'color': PlotColor.MAGENTA, 'marker': PlotMarker.POINT},
    'cylinder': {'color': PlotColor.YELLOW, 'marker': PlotMarker.X}
}

DATASETS_DICT = {
    'white_only': {'color': PlotColor.BLUE, 'marker': PlotMarker.PLUS},
    'gradient': {'color': PlotColor.GREEN, 'marker': PlotMarker.POINT},
    'white_noise': {'color': PlotColor.RED, 'marker': PlotMarker.X}
}

ALTERNATING_BACKGROUND_LIGHT_DATASETS_DICT = {
    'white_noise': {'color': PlotColor.BLUE, 'marker': PlotMarker.POINT, "background_value": [0]},
    'white_noise_background_636363FF': {'color': PlotColor.TEAL, 'marker': PlotMarker.PLUS, "background_value": [109, 110]},
    'white_noise_background_A5A5A5FF': {'color': PlotColor.GREEN, 'marker': PlotMarker.X, "background_value": [163, 164, 165]},
    'white_noise_background_CFCFCFFF': {'color': PlotColor.MAGENTA, 'marker': PlotMarker.STAR, "background_value": [186, 187, 188]},
    'white_noise_background_F0F0F0FF': {'color': PlotColor.YELLOW, 'marker': PlotMarker.THIN_DIAMOND, "background_value": [200, 201]}
}
