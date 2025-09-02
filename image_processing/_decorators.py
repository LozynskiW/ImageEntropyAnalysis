from functools import wraps
from inspect import signature

from image_processing.basictools.utilities import show_image
from image_processing.model import Profile


def before_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        bound_args = signature(func).bind(*args, **kwargs)
        bound_args.apply_defaults()
        arg_dict = bound_args.arguments
        img = arg_dict.get('img', None)

        self_instance = args[0]
        profile = getattr(self_instance, '_ImageSegmentationSystem__profile', Profile.SILENT)

        match profile:
            case Profile.VERBOSE:
                print(f"Entering: {func.__name__}")
            case Profile.SHOW_IMAGE:
                show_image(img, f"image before {func.__name__}")
            case Profile.VERBOSE_AND_SHOW_IMAGE:
                print(f"Entering: {func.__name__}")
                show_image(img, f"image before {func.__name__}")
            case Profile.SILENT:
                pass
        return func(*args, **kwargs)

    return wrapper
