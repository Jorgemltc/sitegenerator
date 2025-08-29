import os
import shutil
import sys
from gencontent import generate_pages_recursive
from textnode import *

def main():
    #handle_files()
    basepath = "/" if len(sys.argv) <= 1 else sys.argv[1]
    handle_files(basepath)
    

def handle_files(basepath):
    content_root = "./content"
    deploy_root = "./docs"
    static_root = "./static"

    delete_folder(deploy_root)
    copy_contents(static_root, deploy_root)
    generate_pages_recursive(content_root, "template.html", deploy_root, basepath)
    #generate_page("content/index.md", "template.html", "public/index.html")
        
def delete_folder(delete_target):
    print(f"Deleting {delete_target} directory...")
    if os.path.exists(delete_target):
        shutil.rmtree(delete_target)

def copy_contents(curr_path, destination_path):
    if not os.path.exists(destination_path):
        print(f"Creating: {destination_path}")
        os.mkdir(destination_path)    

    curr_files = os.listdir(curr_path)
    for f in curr_files:
        full_orig_path = os.path.join(curr_path, f)
        full_dest_path = os.path.join(destination_path, f)
        
        if os.path.isfile(full_orig_path):
            print(f"Copying: {full_dest_path}")
            shutil.copy(full_orig_path, full_dest_path)
        else:
            copy_contents(full_orig_path, full_dest_path)

main()