from enum import Enum

from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    ULIST = "Unordered list"
    OLIST = "Ordered list"

def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    return [l.strip() for l in lines if l]

def block_to_block_type(block):
    lines = block.split("\n")
    return_block = BlockType.PARAGRAPH

    hash_tuples = tuple(["#"*(n+1) + " " for n in range(6)])
    if block.startswith(hash_tuples):
        return_block = BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return_block =  BlockType.CODE
    if block.startswith(">"):
        for l in lines: 
            if not l.startswith(">"):
                return return_block
        return_block =  BlockType.QUOTE
    if block.startswith("- "):
        for l in lines: 
            if not l.startswith("- "):
                return return_block
        return_block =  BlockType.ULIST
    if block.startswith("1. "):
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                return return_block
        return_block =  BlockType.OLIST
   
    return return_block

def markdown_to_html_node(markdown):
    node_list = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        node_list.append(block_to_html_node(block_type, block))

    return ParentNode("div", node_list)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children_nodes = list(map(text_node_to_html_node, text_nodes))
    return children_nodes

def block_to_html_node(block_type, block):
    match(block_type):
        case BlockType.PARAGRAPH:
            cleaned_block = block.replace("\n", " ")
            children_nodes = text_to_children(cleaned_block)
            return ParentNode("p", children_nodes)
        
        case BlockType.HEADING:
            hashtag_count = 1
            for i in range(1,6):
                if block[i] != "#":
                    hashtag_count = i
                    break

            cleaned_block = block[hashtag_count + 1:].replace("\n", " ")
            children_nodes = text_to_children(cleaned_block)
            return ParentNode(f"h{hashtag_count}", children_nodes)
        
        case BlockType.CODE:
            inside_text = block.strip("```\n")
            code_node = LeafNode("code", inside_text + "\n")
            return ParentNode("pre", [code_node])

        case BlockType.QUOTE:
            lines = block.split("\n")
            clean_lines = " ".join([line[1:].strip() for line in lines])
            
            children_nodes = text_to_children(clean_lines)
            return ParentNode(f"blockquote", children_nodes)

        case BlockType.ULIST:
            lines = block.split("\n")
            clean_lines = [line[2:] for line in lines]

            children_nodes = [ ParentNode("li", text_to_children(cl)) for cl in clean_lines ]
            return ParentNode("ul", children_nodes)
        
        case BlockType.OLIST:
            lines = block.split("\n")
            clean_lines = [line[3:] for line in lines]

            children_nodes = [ ParentNode("li", text_to_children(cl)) for cl in clean_lines ]
            return ParentNode("ol", children_nodes)
        
        case _ : 
            raise Exception("Invalid block type")