import unittest

from main import *

class TestTitleExtraction(unittest.TestCase):
    
    def test_good_format(self):
        mkdown = """
# title
## and some heading
with a paragraph
"""
        title = extract_title(mkdown)
        self.assertEqual(title, "title")

    def test_no_title(self):
        mkdown = """
## title
## and some heading
with a paragraph
"""
        self.assertRaises(ValueError, extract_title, mkdown)

    def test_no_newline(self):
        mkdown = """# title"""
        title = extract_title(mkdown)
        self.assertEqual(title, "title")

    def test_white_space(self):
        mkdown = """
   #    title          
## and some heading
with a paragraph
"""
        title = extract_title(mkdown)
        self.assertEqual(title, "title")
    
    def test_title_not_on_first_line(self):
        mkdown = """
## some heading
some paragraph
# title
some paragraph
"""
        title = extract_title(mkdown)
        self.assertEqual(title, "title")
    
    def test_multi_word_title(self):
        mkdown = """
# title with multiple words  
## and some heading
with a paragraph
"""
        title = extract_title(mkdown)
        self.assertEqual(title, "title with multiple words")

if __name__ == "__main__":
    unittest.main()