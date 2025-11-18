import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling


class ProjectionSyncer:
    def sync(self, pre_path, post_path, out_path):
        match_file = pre_path
        src_file = post_path
        dst_file = out_path
        with rasterio.open(match_file) as ref:
            dst_crs = ref.crs
            dst_transform, width, height = calculate_default_transform(
                src_file.crs, dst_crs, src_file.width, src_file.height, *src_file.bounds
            )

        kwargs = src_file.meta.copy()
        kwargs.update(
            {
                "crs": dst_crs,
                "transform": dst_transform,
                "width": width,
                "height": height,
            }
        )

        with rasterio.open(dst_file, "w", **kwargs) as dst:
            reproject(
                source=rasterio.band(src_file, 1),
                destination=rasterio.band(dst, 1),
                src_transform=src_file.transform,
                src_crs=src_file.crs,
                dst_transform=dst_transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest,
            )
