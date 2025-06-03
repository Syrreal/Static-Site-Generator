from textnode import *
from htmlnode import *
from textnode_helpers import *

def text_to_text_nodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    delimiters_types = [
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
        ("`", TextType.CODE),
        ]
    new_nodes = []
    for delimiter, text_type in delimiters_types:
        text_nodes = split_nodes_delimiter(text_nodes, delimiter, text_type)
    text_nodes = split_nodes_image(text_nodes)
    return split_nodes_image(text_nodes)

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

def markdown_to_blocks(markdown):
    return list(map(lambda x: x.strip(), markdown.split("\n\n")))

def main():
    a = TextNode("achor text", TextType.LINK, "https://www.google.com")
    b = TextNode("bold text", TextType.BOLD)

    print(a)
    print(b)

if __name__ == "__main__":
    main()