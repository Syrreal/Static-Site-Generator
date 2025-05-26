import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    
    def test_no_prop(self):
        node = HTMLNode("a", "Value", None, None)
        self.assertTrue(node.props_to_html() == None)

    def test_single_prop(self):
        node = HTMLNode("a", "Value", None, {"href": "https://www.google.com"})
        self.assertTrue(node.props_to_html() == ' href="https://www.google.com"')
    
    def test_multi_prop(self):
        node = HTMLNode("a", "Value", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertTrue(node.props_to_html() == ' href="https://www.google.com" target="_blank"')
