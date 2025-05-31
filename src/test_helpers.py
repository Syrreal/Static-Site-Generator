import unittest

from htmlnode import *
from textnode import *
from main import text_node_to_html_node, split_nodes_delimiter


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

class TestSplitNodesDelimiter(unittest.TestCase):
    
    # def test_single_block(self):
    #     starting_nodes = [TextNode("Text with 'code' block", TextType.TEXT)]
    #     new_nodes = split_nodes_delimiter(starting_nodes, "'", TextType.CODE)
    #     self.assertEqual(new_nodes, [
    #                             TextNode('Text with ', TextType.TEXT), 
    #                             TextNode('code', TextType.CODE), 
    #                             TextNode(' block', TextType.TEXT)
    #                             ])

    def test_sequential_blocks(self):
        starting_nodes = [TextNode("Text with _two__italic_ words", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(starting_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
                                TextNode('Text with ', TextType.TEXT), 
                                TextNode('two', TextType.ITALIC),
                                TextNode('italic', TextType.ITALIC), 
                                TextNode(' words', TextType.TEXT)
                                ])
        
    # def test_non_sequential_blocks(self):
    #     starting_nodes = [TextNode("Text with **multiple** bold **lines** that arent right next to eachother", TextType.TEXT)]
    #     new_nodes = split_nodes_delimiter(starting_nodes, "**", TextType.BOLD)
    #     self.assertEqual(new_nodes, [
    #                             TextNode('Text with ', TextType.TEXT), 
    #                             TextNode('multiple', TextType.BOLD),
    #                             TextNode(' bold ', TextType.TEXT),
    #                             TextNode('lines', TextType.BOLD), 
    #                             TextNode(' that arent right next to eachother', TextType.TEXT)
    #                             ])
        
    # def test_incomplete_blocks(self):
    #     starting_nodes = [TextNode("Text with an incomplete 'code block", TextType.TEXT)]
    #     self.assertRaises(SyntaxError, split_nodes_delimiter, starting_nodes, "'", TextType.CODE)

if __name__ == "__main__":
    unittest.main()