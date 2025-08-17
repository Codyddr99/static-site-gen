import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):
    
    def test_heading_h1(self):
        block = "# This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_h6(self):
        block = "###### This is an h6 heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_with_spaces_after_hashes(self):
        block = "##   This has extra spaces"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_not_heading_no_space_after_hash(self):
        block = "#This is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_not_heading_too_many_hashes(self):
        block = "####### This has too many hashes"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_not_heading_hash_in_middle(self):
        block = "This # is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_code_block_simple(self):
        block = "```\nprint('hello')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)
    
    def test_code_block_with_language(self):
        block = "```python\nprint('hello')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)
    
    def test_code_block_multiline(self):
        block = "```\nline 1\nline 2\nline 3\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)
    
    def test_not_code_block_missing_end(self):
        block = "```\nprint('hello')"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_not_code_block_missing_start(self):
        block = "print('hello')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_quote_single_line(self):
        block = "> This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_quote_multiple_lines(self):
        block = "> This is a quote\n> with multiple lines\n> all starting with >"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_quote_with_empty_line(self):
        block = "> Line one\n>\n> Line three"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_not_quote_missing_one_bracket(self):
        block = "> This line has bracket\nThis line doesn't\n> This line has bracket"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_unordered_list_single_item(self):
        block = "- Item one"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_unordered_list_multiple_items(self):
        block = "- Item one\n- Item two\n- Item three"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_unordered_list_with_nested_text(self):
        block = "- Item with **bold** text\n- Item with *italic* text"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_not_unordered_list_missing_space(self):
        block = "-Item without space\n- Item with space"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_not_unordered_list_missing_dash(self):
        block = "- Item with dash\nItem without dash"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_ordered_list_single_item(self):
        block = "1. First item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def test_ordered_list_multiple_items(self):
        block = "1. First item\n2. Second item\n3. Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def test_ordered_list_with_nested_text(self):
        block = "1. Item with **bold** text\n2. Item with `code` text"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def test_not_ordered_list_wrong_starting_number(self):
        block = "2. Starting with 2\n3. Then 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_not_ordered_list_skip_number(self):
        block = "1. First item\n3. Skipped 2"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_not_ordered_list_missing_space(self):
        block = "1.Missing space\n2. Has space"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_not_ordered_list_wrong_format(self):
        block = "1) Wrong punctuation\n2) Also wrong"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_paragraph_plain_text(self):
        block = "This is just a regular paragraph with some text."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_paragraph_multiline(self):
        block = "This is a paragraph\nwith multiple lines\nthat don't match any special format."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_paragraph_with_formatting(self):
        block = "This paragraph has **bold** and *italic* text."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_heading_and_paragraph(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it."""
        blocks = markdown_to_blocks(md)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_multiple_blocks(self):
        md = """# Heading

Paragraph 1

## Subheading

Paragraph 2 with more text

- List item 1
- List item 2

Final paragraph"""
        blocks = markdown_to_blocks(md)
        expected = [
            "# Heading",
            "Paragraph 1", 
            "## Subheading",
            "Paragraph 2 with more text",
            "- List item 1\n- List item 2",
            "Final paragraph"
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """# Heading



Paragraph with excessive newlines around it



- List item


Final text"""
        blocks = markdown_to_blocks(md)
        expected = [
            "# Heading",
            "Paragraph with excessive newlines around it",
            "- List item",
            "Final text"
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_whitespace_handling(self):
        md = """   # Heading with leading spaces   

  Paragraph with leading and trailing spaces  

- List item with spaces  """
        blocks = markdown_to_blocks(md)
        expected = [
            "# Heading with leading spaces",
            "Paragraph with leading and trailing spaces",
            "- List item with spaces"
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_single_block(self):
        md = "Just a single paragraph with no double newlines"
        blocks = markdown_to_blocks(md)
        expected = ["Just a single paragraph with no double newlines"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        expected = []
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        expected = []
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_mixed_block_types(self):
        md = """# Main Heading

This is a regular paragraph.

## Subheading

Another paragraph with **formatting**.

> This is a blockquote
> with multiple lines

```
code block
with multiple lines
```

1. Numbered list
2. Second item

- Bullet list
- Another bullet

Final paragraph at the end."""
        blocks = markdown_to_blocks(md)
        expected = [
            "# Main Heading",
            "This is a regular paragraph.",
            "## Subheading", 
            "Another paragraph with **formatting**.",
            "> This is a blockquote\n> with multiple lines",
            "```\ncode block\nwith multiple lines\n```",
            "1. Numbered list\n2. Second item",
            "- Bullet list\n- Another bullet",
            "Final paragraph at the end."
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_preserve_single_newlines(self):
        # Single newlines within blocks should be preserved
        md = """First line of paragraph
Second line of same paragraph

Different paragraph
Also multiple lines
In the same paragraph"""
        blocks = markdown_to_blocks(md)
        expected = [
            "First line of paragraph\nSecond line of same paragraph",
            "Different paragraph\nAlso multiple lines\nIn the same paragraph"
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_tabs_and_spaces(self):
        md = """\t# Heading with tab

  Paragraph with spaces

\tAnother paragraph with tab"""
        blocks = markdown_to_blocks(md)
        expected = [
            "# Heading with tab",
            "Paragraph with spaces",
            "Another paragraph with tab"
        ]
        self.assertEqual(blocks, expected)


if __name__ == "__main__":
    unittest.main()
