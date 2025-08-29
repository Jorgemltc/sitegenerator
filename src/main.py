import os
import shutil
from gencontent import generate_pages_recursive
from textnode import *

def main():
    handle_files()

def handle_files():
    public_root = "./public"
    static_root = "./static"

    delete_public()
    copy_contents(static_root, public_root)
    generate_pages_recursive("./content", "template.html", "./public")
    #generate_page("content/index.md", "template.html", "public/index.html")
        
def delete_public():
    public_root = "./public"
    print("Deleting public directory...")
    if os.path.exists(public_root):
        shutil.rmtree(public_root)

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