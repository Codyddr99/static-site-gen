import unittest
from block_markdown import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_headings(self):
        md = """
# This is an h1

## This is an h2

### This is an h3 with **bold** text

#### This is an h4

##### This is an h5

###### This is an h6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>This is an h1</h1><h2>This is an h2</h2><h3>This is an h3 with <b>bold</b> text</h3><h4>This is an h4</h4><h5>This is an h5</h5><h6>This is an h6</h6></div>"
        self.assertEqual(html, expected)
    
    def test_quote_block(self):
        md = """
> This is a quote
> with multiple lines
> and some **bold** text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a quote with multiple lines and some <b>bold</b> text</blockquote></div>"
        self.assertEqual(html, expected)
    
    def test_quote_block_single_line(self):
        md = "> Just one line of quote with _italic_ text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>Just one line of quote with <i>italic</i> text</blockquote></div>"
        self.assertEqual(html, expected)
    
    def test_unordered_list(self):
        md = """
- First item with **bold**
- Second item with _italic_
- Third item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>First item with <b>bold</b></li><li>Second item with <i>italic</i></li><li>Third item with <code>code</code></li></ul></div>"
        self.assertEqual(html, expected)
    
    def test_ordered_list(self):
        md = """
1. First item
2. Second item with **bold**
3. Third item with [a link](http://example.com)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><ol><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <a href="http://example.com">a link</a></li></ol></div>'
        self.assertEqual(html, expected)
    
    def test_mixed_block_types(self):
        md = """
# Main Heading

This is a paragraph with **bold** text.

## Subheading

> This is a quote block

```
def hello():
    print("Hello, world!")
```

- List item one
- List item two

1. Ordered item one
2. Ordered item two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # Check that it contains the expected structure
        self.assertIn("<div>", html)
        self.assertIn("<h1>Main Heading</h1>", html)
        self.assertIn("<p>This is a paragraph with <b>bold</b> text.</p>", html)
        self.assertIn("<h2>Subheading</h2>", html)
        self.assertIn("<blockquote>This is a quote block</blockquote>", html)
        self.assertIn('<pre><code>def hello():\n    print("Hello, world!")\n</code></pre>', html)
        self.assertIn("<ul><li>List item one</li><li>List item two</li></ul>", html)
        self.assertIn("<ol><li>Ordered item one</li><li>Ordered item two</li></ol>", html)
        self.assertIn("</div>", html)
    
    def test_empty_markdown(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")
    
    def test_whitespace_only_markdown(self):
        md = "   \n\n   \n   "
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")
    
    def test_single_word_paragraph(self):
        md = "Hello"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>Hello</p></div>")
    
    def test_code_block_with_language_specifier(self):
        md = """
```python
def greet():
    return "Hello"
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><pre><code>python\ndef greet():\n    return "Hello"\n</code></pre></div>'
        self.assertEqual(html, expected)
    
    def test_paragraph_with_images_and_links(self):
        md = """
This paragraph has an ![image](http://example.com/img.png) and a [link](http://example.com).
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><p>This paragraph has an <img src="http://example.com/img.png" alt="image"></img> and a <a href="http://example.com">link</a>.</p></div>'
        self.assertEqual(html, expected)
    
    def test_multiline_paragraph(self):
        md = """
This is a paragraph
that spans multiple lines
and should be joined with spaces.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><p>This is a paragraph that spans multiple lines and should be joined with spaces.</p></div>"
        self.assertEqual(html, expected)


if __name__ == "__main__":
    unittest.main()
