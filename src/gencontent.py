import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as from_file:
        from_file_string = from_file.read()

    with open(template_path, "r") as template_file:
        template_file_string = template_file.read()

    html_node = markdown_to_html_node(from_file_string)
    html_node_string = html_node.to_html()
    markdown_title = extract_title(from_file_string)
    
    executed_template = template_file_string.replace("{{ Title }}", markdown_title)
    executed_template = executed_template.replace("{{ Content }}", html_node_string)
    executed_template = executed_template.replace('href="/', f'href="{basepath}')
    executed_template = executed_template.replace('src="/', f'src="{basepath}')

    with open(dest_path, "a") as f:
        f.write(executed_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        print(f"Creating: {dest_dir_path}")
        os.mkdir(dest_dir_path)    

    curr_files = os.listdir(dir_path_content)
    for f in curr_files:
        full_orig_path = os.path.join(dir_path_content, f)
        full_dest_path = os.path.join(dest_dir_path, f)
        
        if os.path.isfile(full_orig_path):
            #new_dest_path = Path(full_dest_path).with_suffix(".html")
            #generate_page(full_orig_path, template_path, new_dest_path, basepath)
            root_orig, ext_orig = os.path.splitext(full_orig_path)
            if ext_orig == ".md":
                root_dest, ext_dest = os.path.splitext(full_dest_path)
                new_html_file = root_dest + ".html"
                generate_page(full_orig_path, template_path, new_html_file, basepath)
        else:
            generate_pages_recursive(full_orig_path, template_path, full_dest_path, basepath)

#def generate_html_from_template()