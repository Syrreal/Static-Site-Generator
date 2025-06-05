from blocktype import *
from htmlnode import *
from textnode import *
from helpers import *

def markdown_to_blocks(markdown):
    blocks = list(map(lambda x: x.strip(), markdown.split("\n\n")))
    # Return non-empty blocks
    return [block for block in blocks if block]

def trim_block(block, block_type) -> list:
    "Function returns a list with elements having type identifiers trimmed"
    if block_type == BlockType.HEADING:
        # Leading # for heading ends at first white space
        # number of #'s = heading size (1-6) for tag
        heading_size = len(block.split(" ")[0])
        return [block[:heading_size]]
    if block_type == BlockType.CODE:
        # code will have 3 back ticks on either side
        return [block[3:-3].strip()]
    if block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        # each line will be led with "#. "
        return [line[3:] for line in lines if line]
    if block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        # each line will be led with "- "
        return [line[2:] for line in lines if line]
    if block_type == BlockType.QUOTE:
        lines = block.split("\n")
        # each line will be led with ">"
        # Rejoin lines with a space rather than a newline
        return [" ".join([line[1:] for line in lines])]
    if block_type == BlockType.PARAGRAPH:
        # Replace newlines with spaces
        return [block.replace("\n", " ")]

def create_parent(block, block_type):
    if block_type == BlockType.HEADING:
        # Leading # for heading ends at first white space
        # number of #'s = heading size (1-6) for tag
        heading_size = len(block.split(" ")[0])
        return ParentNode(f'h{heading_size}', None)
    if block_type == BlockType.CODE:
        return ParentNode("code", None)
    if block_type == BlockType.ORDERED_LIST:
        return ParentNode("ul", None)
    if block_type == BlockType.UNORDERED_LIST:
        return ParentNode("ol", None)
    if block_type == BlockType.QUOTE:
        return ParentNode("blockquote", None)
    if block_type == BlockType.PARAGRAPH:
        return ParentNode("p", None)

def text_to_children(text):
    nodes = []
    # if text is list of len > 1 then its a list block type
    if len(text) > 1:
        for node in text:
            # Create a parent <li> tag for each item
            parent = ParentNode("li")
            # Convert text to a list of text nodes, then convert text nodes into html nodes
            children = list(map(lambda x: text_node_to_html_node(x), text_to_text_nodes(node)))
            # Add nodes to parent li node
            parent.children = children
            nodes.append(parent)
    else:
        # if text is only 1 element convert text directly into nodes
        # Convert text to text nodes and then into html nodes before adding them to the list
        nodes.extend(map(lambda x: text_node_to_html_node(x) ,text_to_text_nodes(text[0])))
    return nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    # Create grandparent with an empty list to add blocks to
    grandparent = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_block_type(block)
        # Parent MUST be created before block is trimmed
        parent = create_parent(block, block_type)
        # Trim block type indicators off of block text so they dont appear in children
        trimmed_block = trim_block(block, block_type)
        # Code blocks are processed differently than the rest of the block types
        if block_type == BlockType.CODE:
            # Code text should not be processed
            child = text_node_to_html_node(TextNode(trimmed_block[0], TextType.TEXT))
            parent.children = [child]
            # Code blocks should be under an aditional "<pre>" parent node
            parent = ParentNode("pre", [parent])
        else:
            children = text_to_children(trimmed_block)
            parent.children = children
        # Add block to grandparent
        grandparent.children.append(parent)
    return grandparent
            