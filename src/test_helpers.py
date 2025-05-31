import unittest

from htmlnode import *
from textnode import *
from main import *


class TestTextToHTML(unittest.TestCase):
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
    
    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
    
    def test_code(self):
        node = TextNode("This is code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code text")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
    
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "img.src")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "img.src", "alt": "This is an image"})
    
    def test_empty_bold(self):
        node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")

class TestExtractLinks(unittest.TestCase):
    def test_extract_one_link(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://link.com)"
        )
        self.assertListEqual([("link", "https://link.com")], matches)
    
    def test_extract_multi_link(self):
        matches = extract_markdown_links(
            "This is text with one [link](https://link.com/link)" \
            "and a second [link2](https://link.com/link2)"
        )
        self.assertListEqual([("link", "https://link.com/link"), ("link2", "https://link.com/link2")], matches)
    
    def test_extract_bad_format(self):
        matches = extract_markdown_links(
            "This is a text with [link](https://link.com/badformat/"
        )
        self.assertListEqual([], matches)

    def test_extract_good_and_bad_formats(self):
        matches = extract_markdown_links(
            "This is a text with [link](https://link.com)" \
            " and ![link2](https://link.com/badformat/"
        )
        self.assertListEqual([("link", "https://link.com")], matches)

    def test_extract_image_and_link(self):
        matches = extract_markdown_links(
            "This is a text with an ![image](https://image.com/image.gif)" \
            "and a [link](https://link.com/)"
        )
        self.assertListEqual([("link", "https://link.com/")], matches)

class TestExtractImages(unittest.TestCase):
    def test_extract_one_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_multi_image(self):
        matches = extract_markdown_images(
            "This is text with one ![image](https://image.com/image1.gif)" \
            "and a second ![image2](https://image.com/image2.png)"
        )
        self.assertListEqual([("image", "https://image.com/image1.gif"), ("image2", "https://image.com/image2.png")], matches)
    
    def test_extract_bad_format(self):
        matches = extract_markdown_images(
            "This is a text with ![image](https://image.com/badformat.jpg"
        )
        self.assertListEqual([], matches)

    def test_extract_good_and_bad_formats(self):
        matches = extract_markdown_images(
            "This is a text with ![image](https://image.com/goodformat.jpg)" \
            " and ![image2](https://image.com/badformat.gif"
        )
        self.assertListEqual([("image", "https://image.com/goodformat.jpg")], matches)

    def test_extract_image_and_link(self):
        matches = extract_markdown_images(
            "This is a text with an ![image](https://image.com/image.gif)" \
            "and a [link](https://link.com/)"
        )
        self.assertListEqual([("image", "https://image.com/image.gif")], matches)

class TestSplitNodes(unittest.TestCase):
    
    # Delimiter splitting tests
    def test_single_block(self):
        starting_nodes = [TextNode("Text with 'code' block", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(starting_nodes, "'", TextType.CODE)
        self.assertEqual(new_nodes, [
                                TextNode('Text with ', TextType.TEXT), 
                                TextNode('code', TextType.CODE), 
                                TextNode(' block', TextType.TEXT)
                                ])

    def test_sequential_blocks(self):
        starting_nodes = [TextNode("Text with _two__italic_ words", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(starting_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
                                TextNode('Text with ', TextType.TEXT), 
                                TextNode('two', TextType.ITALIC),
                                TextNode('italic', TextType.ITALIC), 
                                TextNode(' words', TextType.TEXT)
                                ])
        
    def test_non_sequential_blocks(self):
        starting_nodes = [TextNode("Text with **multiple** bold **lines** that arent right next to eachother", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(starting_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
                                TextNode('Text with ', TextType.TEXT), 
                                TextNode('multiple', TextType.BOLD),
                                TextNode(' bold ', TextType.TEXT),
                                TextNode('lines', TextType.BOLD), 
                                TextNode(' that arent right next to eachother', TextType.TEXT)
                                ])
        
    def test_incomplete_blocks(self):
        starting_nodes = [TextNode("Text with an incomplete 'code block", TextType.TEXT)]
        self.assertRaises(SyntaxError, split_nodes_delimiter, starting_nodes, "'", TextType.CODE)

    # Link splitting tests
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link2](https://i.imgur.com/3elNhQu.png) and post text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link2", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and post text", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_split_consecutive_links(self):
        node = TextNode("Text with [link](https://link.com)[link2](https://link.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://link.com"),
                TextNode("link2", TextType.LINK, "https://link.com")
            ],
            new_nodes
        )

    # Image splitting tests
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and post text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and post text", TextType.TEXT)
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()