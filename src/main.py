import shutil
import pathlib
import re
import os

from markdowntohtml import markdown_to_html_node

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
    print("Moving tree ------------------")
    move_children(source, dest)
    print("Finished ---------------------")

def extract_title(markdown):
    title = re.findall(r"(?<!#)#{1}(?!#)[^#].*", markdown)
    if not title:
        raise ValueError("Markdown missing h1 header")
    return title[0].removeprefix("#").strip()

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from "{from_path}" to "{dest_path}" using "{template_path}"')
    md = None
    template = None
    with open(from_path, "+r") as f:
        md = f.read()
    with open(template_path, "+r") as f:
        template = f.read()
    
    title = extract_title(md)
    html = markdown_to_html_node(md).to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    print("Creating destination path")
    # Remove file from dest_path before creating parent directory(s)
    # re.split leaves an empty string in this case so we filter it out before assigning variables
    parent_path, filename = filter(None, re.split(r"\/([\w\_\-\s]*\.[\w]*)", dest_path))

    pathlib.Path(parent_path).mkdir(parents=True, exist_ok=True)
    print("Writing content to dest")
    with open(dest_path, "+x") as dest:
        # write our overridden template file to destination
        dest.write(template)
    print("Finished -----------------------")

def main():
    copy_source_to_dest("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")

if __name__ == "__main__":
    main()