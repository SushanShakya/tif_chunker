from src.chunk_sticher import ChunkSticher
from src.single_chunk_cleaner import SingleChunkCleaner
from src.intersection_window_computer import IntersectionWindowComputer
from src.projection_syncer import ProjectionSyncer
from src.alignment_checker import AlignmentChecker
from src.tiff_chunker import TiffChunker
import numpy as np


def main():

    TILE_SIZE = 1024

    # limit = 10
    limit = None
    pre = "assets/pre_flood.tif"
    pre_out = "chunks/pre"
    post = "assets/post_flood.tif"
    post_out = "chunks/post"

    c1 = TiffChunker(pre, pre_out, tile_size=TILE_SIZE)
    c1.chunk_and_save_tif(limit=limit)
    c1.chunk_and_save_png(limit=limit)

    # c1 = TiffChunker(
    #     post,
    #     post_out,
    #     reference_path=f"{pre_out}/meta",
    #     tile_size=TILE_SIZE,
    # )
    # c1.chunk_and_save_tif(limit=limit)
    # c1.chunk_and_save_png(limit=limit)

    # SingleChunkCleaner(pre_out, post_out).clean()

    ## ---- SECTION : Stiching Chunks Together -----

    # ChunkSticher(
    #     input_dir_path=f"{pre_out}/meta", out_path="chunks/pre/stiched"
    # ).stich()

    # ChunkSticher(
    #     input_dir_path=f"{post_out}/meta", out_path="chunks/post/stiched"
    # ).stich()

    ## ---- SECTION END -----

    # a = np.array(
    #     [
    #         [
    #             [1, 1, 1, 1],
    #             [1, 1, 1, 1],
    #             # [1, 1, 1, 1],
    #             # [1, 1, 1, 1],
    #             [2, 2, 2, 2],
    #             [2, 2, 2, 2],
    #         ],
    #         [
    #             [2, 2, 2, 2],
    #             [2, 2, 2, 2],
    #             [2, 2, 2, 2],
    #             [2, 2, 2, 2],
    #         ],
    #         [
    #             [3, 3, 3, 3],
    #             [3, 3, 3, 3],
    #             [3, 3, 3, 3],
    #             [3, 3, 3, 3],
    #         ],
    #         [
    #             [4, 4, 4, 4],
    #             [4, 4, 4, 4],
    #             [4, 4, 4, 4],
    #             [4, 4, 4, 4],
    #         ],
    #     ]
    # )

    # r = a[0, :, :]
    # print(r == 1)
    # print((r == 1).mean())


if __name__ == "__main__":
    main()
