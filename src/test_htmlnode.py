import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    
    # HTML node "props to html" tests
    def test_no_prop(self):
        node = HTMLNode("a", "Value", None, None)
        self.assertTrue(node.props_to_html() == None)

    def test_single_prop(self):
        node = HTMLNode("a", "Value", None, {"href": "https://www.google.com"})
        self.assertTrue(node.props_to_html() == ' href="https://www.google.com"')
    
    def test_multi_prop(self):
        node = HTMLNode("a", "Value", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertTrue(node.props_to_html() == ' href="https://www.google.com" target="_blank"')

    # Leaf node "to html" tests
    def test_leaf_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_a(self):
        node = LeafNode("a", "Link text", {"href": "https://www.google.com"}) 
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Link text</a>')
    
    def test_leaf_no_tag(self):
        node = LeafNode(None, "Text with no tag")
        self.assertEqual(node.to_html(), "Text with no tag")
