import unittest
from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    
    def test_simple_title(self):
        markdown = "# Hello World"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")
    
    def test_title_with_extra_whitespace(self):
        markdown = "#   Hello World   "
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")
    
    def test_title_in_middle_of_content(self):
        markdown = """
Some introductory text here.

# Main Title

This is the body content.
"""
        result = extract_title(markdown)
        self.assertEqual(result, "Main Title")
    
    def test_title_with_leading_whitespace(self):
        markdown = "   # Indented Title"
        result = extract_title(markdown)
        self.assertEqual(result, "Indented Title")
    
    def test_first_h1_is_returned(self):
        markdown = """
# First Title

Some content here.

# Second Title

More content.
"""
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")
    
    def test_title_with_special_characters(self):
        markdown = "# Welcome to My Blog! 🎉"
        result = extract_title(markdown)
        self.assertEqual(result, "Welcome to My Blog! 🎉")
    
    def test_title_with_markdown_formatting(self):
        markdown = "# **Bold** and _Italic_ Title"
        result = extract_title(markdown)
        self.assertEqual(result, "**Bold** and _Italic_ Title")
    
    def test_empty_title(self):
        markdown = "#"
        result = extract_title(markdown)
        self.assertEqual(result, "")
    
    def test_title_with_only_space(self):
        markdown = "# "
        result = extract_title(markdown)
        self.assertEqual(result, "")
    
    def test_no_h1_header_raises_exception(self):
        markdown = """
## This is an h2
### This is an h3
#### This is an h4

Some content without any h1.
"""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("No h1 header found", str(context.exception))
    
    def test_empty_markdown_raises_exception(self):
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_whitespace_only_markdown_raises_exception(self):
        markdown = "   \n\n   \n"
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_h1_without_space_is_not_recognized(self):
        markdown = "#NoSpace"
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_multiple_hash_symbols_not_h1(self):
        markdown = """
## Not an h1
### Also not an h1
#### Still not an h1
"""
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_hash_in_middle_of_line_not_h1(self):
        markdown = "This line has a # in the middle"
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_title_at_end_of_document(self):
        markdown = """
Some content here.
More content.

# Final Title"""
        result = extract_title(markdown)
        self.assertEqual(result, "Final Title")
    
    def test_title_with_numbers_and_symbols(self):
        markdown = "# Chapter 1: Getting Started (Version 2.0)"
        result = extract_title(markdown)
        self.assertEqual(result, "Chapter 1: Getting Started (Version 2.0)")


if __name__ == "__main__":
    unittest.main()
