import unittest

from blocktype import block_to_block_type, BlockType

class TestBlockType(unittest.TestCase):

    def test_heading_1(self):
        block = "# heading"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_heading_6(self):
        block = "###### heading"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))
    
    def test_code(self):
        block = "```code block```"
        self.assertEqual(BlockType.CODE, block_to_block_type(block))
    
    def test_code_multiline(self):
        block = """```code block
on multiple lines
with f/u.n~k`y
characters```"""
        self.assertEqual(BlockType.CODE, block_to_block_type(block))
    
    def test_quote_single(self):
        block = ">Quote"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))
    
    def test_quote_multi(self):
        block = """>quotes
>on
>lots
>of
>lines
>:)"""
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))
    
    def test_unordered_single(self):
        block = "- unordered list"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_unordered_multi(self):
        block = """- unordered
- list
- on
- multiple
- lines
- ^~^"""
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_ordered_single(self):
        block = "1. ordered list"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_ordered_multi(self):
        block = """1. multi
2. line
3. ordered
4. list
5. :O"""
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_paragraph(self):
        block = "this is a paragraph"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_fail_heading(self):
        block = "####### too many pound signs heading"
        self.assertNotEqual(BlockType.HEADING, block_to_block_type(block))

if __name__ == "__main__":
    unittest.main()