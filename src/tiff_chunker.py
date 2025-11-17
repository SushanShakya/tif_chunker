import rasterio
from rasterio.windows import Window
import numpy as np
from PIL import Image
import json
import os


class TiffChunker:
    def __init__(self, tiff_path, out_dir, tile_size=1024):
        self.tiff_path = tiff_path
        self.tile_size = tile_size
        self.src = rasterio.open(self.tiff_path)
        self.out_dir = out_dir

    def src_info(self):
        print(self.src.count)
        print(self.src.shape)

    def save_as_png(self, i, j, tile):
        tile = np.transpose(tile, (1, 2, 0))

        # Ensure dtype is uint8
        tile = tile.astype(np.uint8)

        # Save as PNG
        img = Image.fromarray(tile)
        out_name = os.path.join(self.out_dir, f"img/tile_{i}_{j}.png")
        img.save(out_name)

    # def save_as_tiff(self, tile):
    #     transform = src.window_transform(window)

    #     profile = src.profile.copy()
    #     profile.update(
    #         {"height": win_height, "width": win_width, "transform": transform}
    #     )

    #     out_name = os.path.join(output_dir, f"img/tile_{i}_{j}.tif")
    #     with rasterio.open(out_name, "w", **profile) as dst:
    #         dst.write(tile)

    def create_tile(self, i, j):
        src = self.src
        tile_size = self.tile_size
        win_width = min(tile_size, src.width - j)
        win_height = min(tile_size, src.height - i)
        window = Window(j, i, win_width, win_height)
        tile = src.read(window=window)
        return tile

    def chunk(self):
        for i in range(0, self.src.height, self.tile_size):
            for j in range(0, self.src.width, self.tile_size):
                tile = self.create_tile(i, j)
                yield tile
