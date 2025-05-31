from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # TEXT texttype does not have a delimiter and does not need to be split
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            # Split with max of 2 splits
            # If text has opening and closing delimiters we should get a 3 element list
            text = node.text.split(delimiter, 2)
            if len(text) == 2:
                raise SyntaxError(f'Missing closing delimiter: {node}')
            elif len(text) == 1:
                # If only 1 element in list that means there are no delimiters left
                # We can return the rest of the text as is
                new_nodes.append(TextNode(text[0], TextType.TEXT))
            else:
                new_nodes.extend([
                    TextNode(text[0], TextType.TEXT), 
                    TextNode(text[1], text_type)
                    ])
                # Call the function again on the remaining text to check for more delimiters
                new_nodes.extend(split_nodes_delimiter([TextNode(text[-1], TextType.TEXT)], delimiter, text_type))
    # Filter out empty nodes in case a delimiter was the first or last character in the original text
    filtered_nodes = [node for node in new_nodes if node.text]
    return filtered_nodes


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

def main():
    a = TextNode("achor text", TextType.LINK, "https://www.google.com")
    b = TextNode("bold text", TextType.BOLD)

    print(a)
    print(b)

if __name__ == "__main__":
    main()