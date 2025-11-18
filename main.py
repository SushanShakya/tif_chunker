from src.intersection_window_computer import IntersectionWindowComputer
from src.projection_syncer import ProjectionSyncer
from src.alignment_checker import AlignmentChecker
from src.tiff_chunker import TiffChunker
import numpy as np


def main():

    TILE_SIZE = 1024

    limit = 10
    # limit = None
    pre = "assets/pre_flood.tif"
    pre_out = "chunks/pre"
    post = "assets/post_flood.tif"
    post_out = "chunks/post"

    w1 = None
    w2 = None

    c1 = TiffChunker(pre, pre_out, tile_size=TILE_SIZE)
    c1.chunk_and_save_tif(window=w1, limit=limit)
    c1.chunk_and_save_png(window=w1, limit=limit)

    c1 = TiffChunker(
        post,
        post_out,
        reference_path=f"{pre_out}/meta",
        tile_size=TILE_SIZE,
    )
    c1.chunk_and_save_tif(window=w2, limit=limit)
    c1.chunk_and_save_png(window=w2, limit=limit)


if __name__ == "__main__":
    main()
