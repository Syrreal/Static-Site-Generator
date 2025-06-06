from markdowntohtml import *
import os
import shutil
import pathlib

def move_children(source, dest):
    print(f'Checking for children in: {source}')
    for child in os.listdir(source):
        # if child is dir - update path, check for grandchildren
        child_dir = os.path.join(source, child)
        dest_dir = os.path.join(dest, child)
        if os.path.isdir(child_dir):
            print(f'    Child({child_dir}) is directory, making directory in destination: {dest_dir}')
            os.mkdir(dest_dir)
            move_children(child_dir, dest_dir)
        # If child is file - add file to destination dir
        else:
            print(f'    Child({child_dir}) is file, moving file to destination {dest_dir}')
            # copy content from source to destination
            shutil.copy(child_dir, dest_dir)

def copy_source_to_dest(source, dest):
    # Check destination and source exist and are directories
    if not os.path.exists(source) and os.path.isdir(source):
        raise ValueError("Invalid source path")
    if not os.path.exists(dest) and os.path.isdir(dest):
        raise ValueError("Invalid destination path")

    # Clear destination directory
    print(f'Clearing destination: {dest}')
    try:
        shutil.rmtree(dest)
    except FileNotFoundError:
        pass
    os.mkdir(dest)

    # Call recursive function to move tree
    print("Moving tree -----------")
    move_children(source, dest)


def main():
    pass

if __name__ == "__main__":
    main()