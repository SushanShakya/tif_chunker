import rasterio
from rasterio.windows import Window, from_bounds
import numpy as np
from PIL import Image
import json
import os


class TiffChunker:
    def __init__(self, tiff_path, out_dir, reference_path=None, tile_size=1024):
        self.tiff_path = tiff_path
        self.tile_size = tile_size
        self.src = rasterio.open(self.tiff_path)
        self.out_dir = out_dir
        self.reference_path = reference_path

    def src_info(self):
        print(self.src.count)
        print(self.src.shape)

    def is_blank(self, tile):
        r = tile[0, :, :]
        g = tile[1, :, :]
        b = tile[2, :, :]
        a = tile[3, :, :]

        return (
            np.all(r == 255)
            and np.all(g == 255)
            and np.all(b == 255)
            and np.all(a == 0)
        )

    def save_as_png(self, i, j, tile):
        tile = np.transpose(tile, (1, 2, 0))

        # Ensure dtype is uint8
        tile = tile.astype(np.uint8)

        # Save as PNG
        img = Image.fromarray(tile)
        out_name = os.path.join(self.out_dir, f"img/tile_{i}_{j}.png")
        img.save(out_name)

    def create_window(self, i, j):
        src = self.src
        tile_size = self.tile_size
        win_width = min(tile_size, src.width - j)
        win_height = min(tile_size, src.height - i)
        return Window(j, i, win_width, win_height)

    def create_tile(self, i, j):
        src = self.src
        window = self.create_window(i, j)
        tile = src.read(window=window)
        return tile

    def total_chunks_possible(self, window=None):
        row_start = 0
        row_stop = self.src.height
        col_start = 0
        col_stop = self.src.width

        if window is not None:
            row_start = int(window.row_off)
            row_stop = int(window.row_off + window.height)
            col_start = int(window.col_off)
            col_stop = int(window.col_off + window.width)

        count = 0

        for i in range(row_start, row_stop, self.tile_size):
            for j in range(col_start, col_stop, self.tile_size):
                count += 1

        return count

    def __chunk(self, window=None):
        row_start = 0
        row_stop = self.src.height
        col_start = 0
        col_stop = self.src.width

        if window is not None:
            row_start = int(window.row_off)
            row_stop = int(window.row_off + window.height)
            col_start = int(window.col_off)
            col_stop = int(window.col_off + window.width)

        for i in range(row_start, row_stop, self.tile_size):
            for j in range(col_start, col_stop, self.tile_size):
                tile = self.create_tile(i, j)
                if self.is_blank(tile):
                    continue
                yield i, j, tile

    def get_files(self, directory):
        all_files = os.listdir(directory)  # gets all files and folders
        return [os.path.join(directory, f) for f in all_files]

    def is_within_bounds(self, bounds):
        tb = bounds
        post_bounds = self.src.bounds
        return (
            tb.left < post_bounds.right
            and tb.right > post_bounds.left
            and tb.bottom < post_bounds.top
            and tb.top > post_bounds.bottom
        )

    def __create_reference_tile(self, bounds):
        tb = bounds
        post_src = self.src
        window = from_bounds(tb.left, tb.bottom, tb.right, tb.top, post_src.transform)
        tile = post_src.read(window=window)
        meta = post_src.meta.copy()
        meta.update(
            {
                "height": tile.shape[1],
                "width": tile.shape[2],
                "transform": rasterio.windows.transform(window, post_src.transform),
            }
        )
        return tile

    def extract_i_j_from_filepath(self, file):
        filename = file.split("/")[-1]
        tmp = filename.split(".")[0].split("_")
        i = int(tmp[1])
        j = int(tmp[2])
        return i, j

    def __chunk_with_reference(self):
        files = self.get_files(self.reference_path)

        for file in files:
            i, j = self.extract_i_j_from_filepath(file)

            with rasterio.open(file) as t:
                bounds = t.bounds

            if self.is_within_bounds(bounds):
                tile = self.__create_reference_tile(bounds)
                yield i, j, tile

    def chunk(self, window=None):
        if self.reference_path is not None:
            return self.__chunk_with_reference()
        return self.__chunk(window)

    def __chunk_and_save(self, on_save, window=None, limit=None):
        count = 0
        chunks = self.chunk(window)
        for i, j, tile in chunks:
            on_save(i, j, tile)
            count += 1
            if count == limit:
                break

    def chunk_and_save_png(self, window=None, limit=None):
        self.__chunk_and_save(self.save_as_png, window=window, limit=limit)

    def save_as_tif(self, i, j, tile):
        window = self.create_window(i, j)
        transform = self.src.window_transform(window)

        profile = self.src.profile.copy()
        win_width = min(self.tile_size, self.src.width - j)
        win_height = min(self.tile_size, self.src.height - i)

        profile.update(
            {
                "height": win_height,
                "width": win_width,
                "transform": transform,
            }
        )

        out_name = os.path.join(self.out_dir, f"meta/tile_{i}_{j}.tif")
        with rasterio.open(out_name, "w", **profile) as dst:
            dst.write(tile)

    def chunk_and_save_tif(self, window=None, limit=None):
        self.__chunk_and_save(self.save_as_tif, window=window, limit=limit)
