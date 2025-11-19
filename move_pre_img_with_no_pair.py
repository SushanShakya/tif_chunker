import os
import shutil

path = "chunks/pre/img"
reference_path = "chunks/post/img"

destination = "chunks/pre/singular"


def get_files(directory):
    all_files = os.listdir(directory)  # gets all files and folders
    return [f.split(".")[0] for f in all_files if f.endswith(".png")]


existing = get_files(reference_path)

pre_files = get_files(path)


def move_file(filename):
    file = f"{path}/{filename}.png"
    shutil.move(file, destination)


for file in pre_files:
    if file in existing:
        continue
    move_file(file)
