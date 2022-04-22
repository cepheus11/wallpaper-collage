from PIL import Image
from pathlib import Path
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-x", "--width", default=1920, help="Collage width in pixels. Default 1920.")
arg_parser.add_argument("-y", "--height", default=1200, help="Collage height in pixels. Default 1200.")
arg_parser.add_argument("-w", "--wallpaper-dir", default="wallpapers",
                        help="Directory with source images. Default wallpapers.")
arg_parser.add_argument("-c", "--collage-dir", default="collage",
                        help="Target directory for collage image. Default collage.")
arg_parser.add_argument("-i", "--interval", default=60,
                        help="Collage change interval in seconds. Minimum 10. Default 60. Set to 0 for no automatic "
                             "change. (Change only once at start, and at signal SIGUSR1)")
arg_parser.add_argument("-m", "--mode", default="single", help="Output mode: single|multiple. Default single.")
arg_parser.add_argument("--debug", help="Print debug messages to stdout. Default 0 (no debug messages).")
args = arg_parser.parse_args()
screen_width = int(args.width)
screen_height = int(args.height)
screen_ar = screen_width / screen_height
wallpaper_dir = args.wallpaper_dir
collage_dir = args.collage_dir
interval = int(args.interval)
if interval == 0:
    auto_change = False
    interval = 3600
else:
    auto_change = True
    if interval < 10:
        interval = 10
output_multiple = args.mode.lower() == "multiple"
jpeg_quality = 95
start_color = "#2D2424"
debug = args.debug


def debug_print(msg):
    global debug
    if debug:
        print(msg)


def debug_print_image_info(img_letter: str, filepath: str, asp_ratio: float):
    filename = Path(filepath).name
    debug_print(f"Image {img_letter}: Aspect Ratio {asp_ratio:.4f}. {filename}")


def aspect_ratio(image: Image) -> float:
    return image.size[0] / image.size[1]


def crop(image: Image, target_ar: float) -> Image:
    """
    Crop the margins of the image out as necessary, according to target aspect ratio.
    :param image: Image object
    :param target_ar: Target aspect ratio. Width / Height
    :return: Image
    """
    current_ar = image.size[0] / image.size[1]
    if target_ar < current_ar:
        # Left and right must be cropped
        new_width = target_ar * image.size[1]
        x1 = round((image.size[0] - new_width) / 2)
        y1 = 0
        x2 = x1 + new_width
        y2 = image.size[1]
    else:
        # Top and bottom must be cropped
        new_height = image.size[0] / target_ar
        x1 = 0
        y1 = round((image.size[1] - new_height) / 2)
        x2 = image.size[0]
        y2 = y1 + new_height

    return image.crop((x1, y1, x2, y2))


def crop_resize(image: Image, target_ar: float, scale_factor: float) -> Image:
    """
    Crop the margins of the image out as necessary, according to target aspect ratio.
    Resize the cropped image to the target size.
    :param image: Image object
    :param target_ar: Target aspect ratio. Width / Height
    :param scale_factor: Resize factor. Greater than 1 if image is enlarged
    :return: Image
    """
    cropped_image = crop(image, target_ar)
    return cropped_image.resize(
        (round(cropped_image.size[0] * scale_factor), round(cropped_image.size[1] * scale_factor)), Image.BICUBIC)
