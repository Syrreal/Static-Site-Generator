import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    
    # Test equal cases
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("Text", TextType.LINK, "https://test.com")
        node2 = TextNode("Text", TextType.LINK, "https://test.com")
        self.assertEqual(node, node2)
    
    # Test not equal cases
    def test_url_neq(self):
        node = TextNode("Text", TextType.LINK, "https://test.com")
        node2 = TextNode("Text", TextType.LINK, "https://test2.com")
        self.assertNotEqual(node, node2)
    
    def test_no_url_neq(self):
        node = TextNode("Text", TextType.LINK, "https://test.com")
        node2 = TextNode("Text", TextType.LINK)
        self.assertNotEqual(node, node2)
    
    


if __name__ == "__main__":
    unittest.main()
