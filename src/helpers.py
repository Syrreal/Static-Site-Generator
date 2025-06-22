import re
from textnode import *
from htmlnode import *

def extract_markdown_images(text):
    # Capture as little text between ![ and ]
    # Capture as little text between ()
    return re.findall(r"!\[(.+?)\]\((.+?)\)", text)

def extract_markdown_links(text):
    # Capture as little text between [ and ] that doesnt have a ! in front
    # Capture as little text between ()
    return re.findall(r"(?<!!)\[(.+?)\]\((.+?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # If the text type is not TEXT then it is already split can be added as is
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            # get a list of all images
            images = extract_markdown_images(node.text)
            # store text in an intermediary to mutate
            text = node.text
            # Gather text splices into a list
            split_text = []
            # Splice text at each image
            for image in images:
                image_str = f'![{image[0]}]({image[1]})'
                # Reform image to extract it from text
                index = text.index(image_str)
                # Append the text before the image into the image and then change
                # the intermediary text to the text after the image
                split_text.append(text[:index])
                text = text[index+len(image_str):]
                # Add the image, as a tuple to differentiate between regular text, to the list
                split_text.append(image)
            # Check if there is any text left over after the last image
            if text:
                # if there is, add it to the list
                split_text.append(text)
            # make nodes from split text list
            for element in split_text:
                # if element is a tuple, its an image otherwise its regular text
                if isinstance(element, tuple):
                    new_nodes.append(TextNode(element[0], TextType.IMAGE, element[1]))
                else:
                    new_nodes.append(TextNode(element, TextType.TEXT))
    # filter out empty nodes
    filtered_nodes = [node for node in new_nodes if node.text]
    return filtered_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # If the text type is not TEXT then it is already split can be added as is
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            # get a list of all links
            links = extract_markdown_links(node.text)
            # store text in an intermediary to mutate
            text = node.text
            # Gather text splices into a list
            split_text = []
            # Splice text at each link
            for link in links:
                link_str = f'[{link[0]}]({link[1]})'
                # Reform link to extract it from text
                index = text.index(link_str)
                # Append the text before the link into the link and then change
                # the intermediary text to the text after the link
                split_text.append(text[:index])
                text = text[index+len(link_str):]
                # Add the link, as a tuple to differentiate between regular text, to the list
                split_text.append(link)
            # Check if there is any text left over after the last link
            if text:
                # if there is, add it to the list
                split_text.append(text)
            # make nodes from split text list
            for text in split_text:
                # if text is in a tuple, its a link otherwise its regular text
                if isinstance(text, tuple):
                    new_nodes.append(TextNode(text[0], TextType.LINK, text[1]))
                else:
                    new_nodes.append(TextNode(text, TextType.TEXT))
    # filter out empty nodes, all link nodes should have urls
    filtered_nodes = [node for node in new_nodes if node.text]
    return filtered_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # If the text type is not TEXT then it is already split can be added as is
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
    return split_nodes_link(text_nodes)

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", text_node.text, {"src": text_node.url})
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
