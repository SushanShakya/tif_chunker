from src.intersection_window_computer import IntersectionWindowComputer
from src.projection_syncer import ProjectionSyncer
from src.alignment_checker import AlignmentChecker
from src.tiff_chunker import TiffChunker
import numpy as np


def main():
    limit = 10
    # limit = None
    pre = "assets/pre_flood.tif"
    pre_out = "chunks/pre"
    post = "assets/post_flood.tif"
    post_out = "chunks/post"

    # c = IntersectionWindowComputer(pre, post)
    # w1, w2 = c.compute()

    w1 = None
    w2 = None

    c1 = TiffChunker(pre, pre_out)
    c1.chunk_and_save_tif(window=w1, limit=limit)
    c1.chunk_and_save_png(window=w1, limit=limit)
    # print(c1.total_chunks_possible(w1))

    c1 = TiffChunker(post, post_out, reference_path=f"{pre_out}/meta")
    c1.chunk_and_save_tif(window=w2, limit=limit)
    c1.chunk_and_save_png(window=w2, limit=limit)
    # print(c1.total_chunks_possible(w2))

    # a = np.array(
    #     [
    #         [
    #             [1, 1, 1, 1],
    #             [1, 1, 1, 1],
    #             [1, 1, 1, 1],
    #             [1, 1, 1, 1],
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
    # r = a[:, :, 0]
    # g = a[:, :, 1]
    # b = a[:, :, 2]
    # a = a[:, :, 3]

    # w = r == 1
    # x = g == 2
    # y = b == 3
    # z = a == 4

    # a = w == w
    # b = a == x
    # c = b == y
    # d = c == z

    # print(np.any(((w == x) == y) == z))
    # print(np.any(d))

    # print(a)

    # AlignmentChecker().check_all()


if __name__ == "__main__":
    main()
