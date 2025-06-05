import unittest

from main import *

class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_heading(self):
        md = """
# This is **bolded** heading
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is **bolded** heading",
            ],
        )

    def test_list(self):
        md = """
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- This is a list\n- with items",
            ],
        )

    def test_multiple_same(self):
        md = """
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

This is a seperate paragraph
that also has multiple lines
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "This is a seperate paragraph\nthat also has multiple lines"
            ],
        )

    def test_multiple(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

- This is another list
- with more items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "- This is another list\n- with more items"
            ],
        )
    def test_trailing_whitespace(self):
        md = """
This is a paragraph

with trailing whitespace

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "with trailing whitespace"
            ]
        )
if __name__ == "__main__":
    unittest.main()