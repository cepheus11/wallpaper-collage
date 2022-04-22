from PIL import Image
from common import aspect_ratio, crop_resize, start_color

# TwoTileLayout is recursive: tile1 and tile2 can be Images, or TwoTileLayouts


class TwoTileLayout:
    def __init__(self, tile1, tile2, vertical=False):
        self.tile1 = tile1
        self.tile2 = tile2
        self.vertical = vertical

    def combined_aspect_ratio(self) -> float:
        if self.vertical:
            inverse_ar1 = 1 / self.tile_aspect_ratio(self.tile1)
            inverse_ar2 = 1 / self.tile_aspect_ratio(self.tile2)
            inverse_ar = inverse_ar1 + inverse_ar2
            return 1 / inverse_ar
        else:
            return self.tile_aspect_ratio(self.tile1) + self.tile_aspect_ratio(self.tile2)

    @staticmethod
    def tile_aspect_ratio(tile) -> float:
        if isinstance(tile, Image.Image):
            return aspect_ratio(tile)
        else:
            assert (isinstance(tile, TwoTileLayout))
            return tile.combined_aspect_ratio()

    # crop factor is the ratio whole_image / cropped_image. Always >= 1
    def crop_factor(self, dimensions: tuple):
        combined_ar = self.combined_aspect_ratio()
        width = dimensions[0]
        height = dimensions[1]
        whole_aspect_ratio = width / height
        if combined_ar > whole_aspect_ratio:
            # left and right must be cropped
            return combined_ar / whole_aspect_ratio
        else:
            # top and bottom must be cropped
            return whole_aspect_ratio / combined_ar

    @staticmethod
    def create_tile(tile, asp_ratio: float, factor: float, dimensions: tuple) -> Image.Image:
        if isinstance(tile, Image.Image):
            resized = crop_resize(tile, asp_ratio, factor)
        else:
            assert(isinstance(tile, TwoTileLayout))
            resized = tile.create_collage(dimensions)
        return resized

    @staticmethod
    def width_of_tile(tile, target_width: float) -> float:
        if isinstance(tile, Image.Image):
            return tile.size[0]
        else:
            assert (isinstance(tile, TwoTileLayout))
            # Inner layout will be rendered with its share of the target screen real estate:
            return target_width
        
    @staticmethod
    def height_of_tile(tile, target_height: float) -> float:
        if isinstance(tile, Image.Image):
            return tile.size[1]
        else:
            assert (isinstance(tile, TwoTileLayout))
            # Inner layout will be rendered with its share of the target screen real estate:
            return target_height

    def create_collage(self, dimensions: tuple) -> Image.Image:
        target_width = dimensions[0]
        target_height = dimensions[1]
        target_aspect_ratio = target_width / target_height
        ar1 = self.tile_aspect_ratio(self.tile1)
        ar2 = self.tile_aspect_ratio(self.tile2)
        combined_ar = self.combined_aspect_ratio()

        # This is not the same crop_factor as in crop_factor(): Might be inverse
        crop_factor = combined_ar / target_aspect_ratio

        if combined_ar > target_aspect_ratio:
            dimension_factor = combined_ar / target_aspect_ratio
        else:
            dimension_factor = target_aspect_ratio / combined_ar

        target_ar1 = ar1 / crop_factor
        target_ar2 = ar2 / crop_factor

        # dim0 is the "main" dimension: Two tiles along dim0 axis
        # dim1 is the "other" dimension: There is only one tile along dim1 axis
        if self.vertical:
            whole_dim1 = target_width
            dim1_1 = self.width_of_tile(self.tile1, target_width)
            dim1_2 = self.width_of_tile(self.tile2, target_width)
            target_dimension_1 = (target_width, target_width / target_ar1)
            target_dimension_2 = (target_width, target_width / target_ar2)
            if combined_ar > target_aspect_ratio:
                # left and right must be cropped
                dim1_factor = dimension_factor
            else:
                # top and bottom must be cropped
                dim1_factor = 1
        else:
            whole_dim1 = target_height
            dim1_1 = self.height_of_tile(self.tile1, target_height)
            dim1_2 = self.height_of_tile(self.tile2, target_height)
                
            target_dimension_1 = (target_height * target_ar1, target_height)
            target_dimension_2 = (target_height * target_ar2, target_height)
            if combined_ar > target_aspect_ratio:
                # left and right must be cropped
                dim1_factor = 1
            else:
                # top and bottom must be cropped
                dim1_factor = dimension_factor

        assert(dim1_factor >= 1)

        # create image1 for tile1:
        fac = whole_dim1 / (dim1_1 / dim1_factor)
        image1 = self.create_tile(self.tile1, target_ar1, fac, target_dimension_1)
        # create image2 for tile2:
        fac = whole_dim1 / (dim1_2 / dim1_factor)
        image2 = self.create_tile(self.tile2, target_ar2, fac, target_dimension_2)
        # result image:
        collage = Image.new("RGB", (round(target_width), round(target_height)), color=start_color)
        # draw image1:
        collage.paste(image1, (0, 0))
        # draw image2:
        if self.vertical:
            y = image1.size[1]
            collage.paste(image2, (0, y))
        else:
            x = image1.size[0]
            collage.paste(image2, (x, 0))
        return collage

    @staticmethod
    def filenames_of_tile(tile) -> list:
        if isinstance(tile, Image.Image):
            return [tile.filename]
        else:
            assert(isinstance(tile, TwoTileLayout))
            return tile.filenames()

    def filenames(self) -> list:
        result = []
        for filename in self.filenames_of_tile(self.tile1):
            result.append(filename)
        for filename in self.filenames_of_tile(self.tile2):
            result.append(filename)
        return result
