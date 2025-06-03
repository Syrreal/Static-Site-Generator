import unittest

from main import *

class TestTextToTextNode(unittest.TestCase):

    def test_full_text(self):
        text = "This is **text** with an _italic_ word and a `code block` " \
        "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://link.com/)"
        text_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://link.com/"),
        ]
        self.assertListEqual(text_nodes, text_to_text_nodes(text))

    def test_multiples(self):
        text = "This is **text** with **LOTS** of _different_ formats and " \
        "_multiples_ of *each* format with ![woah](https://image.com/image.gif)![woah](https://image.com/image.gif)" \
        "[click for MORE](https://more.com/)"
        text_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with ", TextType.TEXT),
            TextNode("LOTS", TextType.BOLD),
            TextNode(" of ", TextType.TEXT),
            TextNode("different", TextType.ITALIC),
            TextNode(" formats and ", TextType.TEXT),
            TextNode("multiples", TextType.ITALIC),
            TextNode(" of ", TextType.TEXT),
            TextNode("each", TextType.BOLD),
            TextNode(" format with ", TextType.TEXT),
            TextNode("woah", TextType.IMAGE, "https://image.com/image.gif"),
            TextNode("woah", TextType.IMAGE, "https://image.com/image.gif"),
            TextNode("click for MORE", TextType.BOLD, "https://more.com")
        ]

if __name__ == "__main__":
    unittest.main()