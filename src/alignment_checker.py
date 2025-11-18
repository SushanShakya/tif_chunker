import os
import rasterio


class AlignmentChecker:
    def get_files(self, directory):
        all_files = os.listdir(directory)  # gets all files and folders
        return [os.path.join(directory, f) for f in all_files if f.endswith(".tif")]

    def pre_tifs(self):
        path = "chunks/pre/meta"
        files = self.get_files(path)
        self.check(files)

    def post_tifs(self):
        path = "chunks/post/meta"
        files = self.get_files(path)
        self.check(files)

    def check(self, files):
        for f in files:
            with rasterio.open(f) as src:
                filename = f.split("/")[-1]
                print(f"{filename}")
                print(src.transform)

    def check_all(self):
        files1 = self.get_files("chunks/pre/meta")
        files2 = self.get_files("chunks/post/meta")
        files = sorted(files1 + files2)
        self.check(files)
