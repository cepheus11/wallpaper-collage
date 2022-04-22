from common import aspect_ratio, crop_resize
from PIL import Image

#   Layout One
#   +---------------+
#   |               |
#   |       A       |
#   |               |
#   +---------------+


class LayoutOne:
    def __init__(self, selected_image: Image.Image):
        self.selected_image = selected_image

    def crop_factor(self, dimensions: tuple):
        ar = aspect_ratio(self.selected_image)
        target_ar = dimensions[0] / dimensions[1]
        if ar > target_ar:
            # left and right must be cropped
            return ar / target_ar
        else:
            # top and bottom must be cropped
            return target_ar / ar

    def create_collage(self, dimensions: tuple):
        ar = aspect_ratio(self.selected_image)
        target_width = dimensions[0]
        target_height = dimensions[1]
        target_ar = target_width / target_height
        if ar > target_ar:
            # left and right must be cropped
            factor = target_height / self.selected_image.size[1]
            resized = crop_resize(self.selected_image, target_ar, factor)
        else:
            # top and bottom must be cropped
            factor = target_width / self.selected_image.size[0]
            resized = crop_resize(self.selected_image, target_ar, factor)
        return resized

    def filenames(self):
        return [self.selected_image.filename]
