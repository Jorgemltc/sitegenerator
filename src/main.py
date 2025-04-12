from textnode import *

def main():
    text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(str(text_node))

main()