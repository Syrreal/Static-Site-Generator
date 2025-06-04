from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    # match 1-6 # characters and any amount of any character after
    if re.fullmatch(r"#{1,6} [\S|\s]*", block):
        return BlockType.HEADING
    # match 3 ` characters with amount of any character after until 3 ` characters 
    elif re.fullmatch(r"`{3}[\S|\s]*`{3}", block):
        return BlockType.CODE
    # Check if all lines in the block have a > as the first character
    elif all(line[0] == ">" for line in block.split("\n")):
        return BlockType.QUOTE
    # Check if all lines in the block have "- " as the start of the line
    elif all(line[:2] == "- " for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    else:
        for i, line in enumerate(block.split("\n")):
            if line[:3] != f'{i+1}. ':
                break
            # If for loop not broken block is an ordered list
            return BlockType.ORDERED_LIST
        # if for loop is broke, no other statements matched, block is a normal paragraph
        return BlockType.PARAGRAPH
