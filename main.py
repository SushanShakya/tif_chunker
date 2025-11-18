from src.intersection_window_computer import IntersectionWindowComputer
from src.projection_syncer import ProjectionSyncer
from src.alignment_checker import AlignmentChecker
from src.tiff_chunker import TiffChunker
import numpy as np


def main():
    limit = 10
    pre = "assets/pre_flood.tif"
    pre_out = "chunks/pre"
    post = "assets/post_flood.tif"
    post_out = "chunks/post"

    c = IntersectionWindowComputer(pre, post)
    w1, w2 = c.compute()

    c1 = TiffChunker(pre, pre_out)
    c1.chunk_and_save_tif(window=w1, limit=limit)
    c1.chunk_and_save_png(window=w1, limit=limit)
    # print(c1.total_chunks_possible(w1))

    c1 = TiffChunker(post, post_out)
    c1.chunk_and_save_tif(window=w2, limit=limit)
    c1.chunk_and_save_png(window=w2, limit=limit)
    # print(c1.total_chunks_possible(w2))

    # AlignmentChecker().check_all()


if __name__ == "__main__":
    main()
