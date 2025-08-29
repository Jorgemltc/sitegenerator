from enum import Enum
from htmlnode import *
# from inline_markdown import (
#     split_nodes_delimiter, 
#     split_nodes_image, 
#     split_nodes_link
# )
# from inline_markdown import (
#     split_nodes_delimiter,
#     extract_markdown_links,
#     extract_markdown_images,
# )

class TextType(Enum):
    TEXT = "text"
    BOLD = "Bold text"
    ITALIC = "Italic text"
    CODE = "Code text"
    LINK = "Links"
    IMAGE = "Images"

class TextNode():
    def __init__(self, text, text_type = TextType.TEXT, url = None): 
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, targetNode):
        return (self.text == targetNode.text and
                self.text_type == targetNode.text_type and
                self.url == targetNode.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT: 
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD: 
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC: 
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE: 
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK: 
        return LeafNode("a", text_node.text, { "href": text_node.url} )
    if text_node.text_type == TextType.IMAGE: 
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")

