import os


class SingleChunkCleaner:
    def __init__(self, pre_dir_path, post_dir_path):
        self.pre_path = pre_dir_path
        self.post_path = post_dir_path

    def get_file_names(self, directory):
        all_files = os.listdir(directory)  # gets all files and folders
        return [f for f in all_files]

    def get_files(self, directory):
        return list(
            map(lambda a: os.path.join(directory, a), self.get_file_names(directory))
        )

    def clean(self):
        for dir in ["img", "meta"]:
            files_with_pair = self.get_file_names(f"{self.post_path}/{dir}")
            cleanup_files = self.get_files(f"{self.pre_path}/{dir}")
            for f in cleanup_files:
                filename = f.split("/")[-1]
                if filename not in files_with_pair:
                    os.remove(f)
