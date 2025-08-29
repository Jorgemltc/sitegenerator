import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes: 
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        
        text_split = node.text.split(delimiter)
        if len(text_split) % 2 == 0: 
            raise Exception("Invalid Markdown syntax")
        
        for i, text_part in enumerate(text_split):
            if text_part == "":
                continue
            val_type = TextType.TEXT if i % 2 == 0 else text_type
            result.append(TextNode(text_part, val_type))

    return result

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes: 
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        
        remaining_text = node.text
        images_split = extract_markdown_images(remaining_text)
        if len(images_split) == 0: 
            result.append(node)
            continue
        
        for image_part in images_split:
            image_alt = image_part[0]
            image_link = image_part[1]
            sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(image_alt, TextType.IMAGE, image_link))
            remaining_text = sections[1]
        if remaining_text != "" :
            result.append(TextNode(remaining_text, TextType.TEXT))
    
    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes: 
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        
        remaining_text = node.text
        url_split = extract_markdown_links(remaining_text)
        if len(url_split) == 0: 
            result.append(node)
            continue
        
        for url_part in url_split:
            url_alt = url_part[0]
            url_link = url_part[1]
            sections = remaining_text.split(f"[{url_alt}]({url_link})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(url_alt, TextType.LINK, url_link))
            remaining_text = sections[1]
        if remaining_text != "":
            result.append(TextNode(remaining_text, TextType.TEXT))
                
    
    return result

def text_to_textnodes(text):
    node_list = [TextNode(text, TextType.TEXT)]
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    return node_list

def extract_markdown_images(text):
    image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_regex, text)
    return matches

def extract_markdown_links(text): 
    links_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(links_regex, text)
    return matches
