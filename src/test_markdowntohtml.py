import unittest
from markdowntohtml import markdown_to_html_node, markdown_to_blocks

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

class TestMarkdownToHTML(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_lists(self):
        md = """
- this
- is
- an
- unordered
- list

1. this
2. list
3. is
4. ordered
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this</li><li>is</li><li>an</li><li>unordered</li><li>list</li></ul><ol><li>this</li><li>list</li><li>is</li><li>ordered</li></ol></div>"
        )
    
    def test_quoteblock(self):
        md = """
>Block
>Quote
> Space
>   
>Empty above
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Block Quote Space\nEmpty above</blockquote></div>"
        )

    def test_heading(self):
        md = """
# This is a heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1></div>"
        )
    
    def test_heading_multi(self):
        md = """
# This is a heading

### This is a smaller heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><h3>This is a smaller heading</h3></div>"
        )

    def test_all(self):
        md = """
# Heading

```
Code**block
```

- unordered
- list

1. ordered
2. list

>Quote

woah
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><pre><code>Code**block</code></pre><ul><li>unordered</li><li>list</li></ul><ol><li>ordered</li><li>list</li></ol><blockquote>Quote</blockquote><p>woah</p></div>"
        )

    def test_empty(self):
        md = """
"""
        self.assertRaises(
            ValueError,
            markdown_to_html_node,
            md
        )

if __name__ == "__main__":
    unittest.main()