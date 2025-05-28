import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
    
    # Parent node "to html" tests
    def test_parent_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_with_props_and_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "Div1"})
        self.assertEqual(parent_node.to_html(),
                         '<div class="Div1"><span>child</span></div>')

    def test_parent_multi_child(self):
        child_node1 = LeafNode("b", "child")
        child_node2 = LeafNode("i", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(),
                         '<div><b>child</b><i>child2</i></div>')
    
    def test_parent_multi_child_and_props(self):
        child_node1 = LeafNode("b", "child")
        child_node2 = LeafNode("i", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2], {"class": "Div1"})
        self.assertEqual(parent_node.to_html(),
                         '<div class="Div1"><b>child</b><i>child2</i></div>')
