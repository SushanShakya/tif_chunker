import rasterio
from rasterio.merge import merge
from rasterio.enums import Resampling
import glob
import os


class ChunkSticher:
    def __init__(self, input_dir_path, out_path):
        self.path = input_dir_path
        self.out_path = out_path
        self.check_and_create_required_dir()

    def check_and_create_required_dir(self):
        from pathlib import Path

        folder = Path(self.out_path)
        folder.mkdir(parents=True, exist_ok=True)

    def stich(self):
        input_folder = self.path
        output_path = f"{self.out_path}/output.tif"
        tifs = glob.glob(os.path.join(input_folder, "*.tif"))

        if not tifs:
            raise ValueError("No .tif files found")

        # open each file
        src_files = [rasterio.open(fp) for fp in tifs]

        # merge with proper geocoordinate alignment
        mosaic, out_transform = merge(src_files, resampling=Resampling.nearest)

        # copy metadata from first file
        out_meta = src_files[0].meta.copy()
        out_meta.update(
            {
                "height": mosaic.shape[1],
                "width": mosaic.shape[2],
                "transform": out_transform,
            }
        )

        # write the final stitched tif
        with rasterio.open(output_path, "w", **out_meta) as dest:
            dest.write(mosaic)

        # cleanup
        for f in src_files:
            f.close()

        return output_path
