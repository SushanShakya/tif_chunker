import rasterio
from rasterio.windows import from_bounds


class IntersectionWindowComputer:
    def __init__(self, pre_path, post_path):
        self.pre_path = pre_path
        self.post_path = post_path

    def compute(self):
        with rasterio.open(self.pre_path) as src1, rasterio.open(
            self.post_path
        ) as src2:
            bounds1, bounds2 = src1.bounds, src2.bounds
            transform1, transform2 = src1.transform, src2.transform

            # 1️⃣ Intersection coordinates (geographic)
            inter_left = max(bounds1.left, bounds2.left)
            inter_bottom = max(bounds1.bottom, bounds2.bottom)
            inter_right = min(bounds1.right, bounds2.right)
            inter_top = min(bounds1.top, bounds2.top)

            if inter_right <= inter_left or inter_top <= inter_bottom:
                raise ValueError("No overlapping area between rasters.")

            # 2️⃣ Convert to windows (pixel coordinates)
            pre_window = (
                from_bounds(
                    inter_left, inter_bottom, inter_right, inter_top, transform1
                )
                .round_offsets()
                .round_shape()
            )
            post_window = (
                from_bounds(
                    inter_left, inter_bottom, inter_right, inter_top, transform2
                )
                .round_offsets()
                .round_shape()
            )

            # 3️⃣ Clip both windows to the same size
            min_height = min(pre_window.height, post_window.height)
            min_width = min(pre_window.width, post_window.width)

            pre_window = pre_window.intersection(
                rasterio.windows.Window(
                    pre_window.col_off, pre_window.row_off, min_width, min_height
                )
            )
            post_window = post_window.intersection(
                rasterio.windows.Window(
                    post_window.col_off, post_window.row_off, min_width, min_height
                )
            )

            return pre_window, post_window
