import unittest
from textnode import TextNode, TextType
from text_to_html import text_node_to_html_node


class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_link_without_url_raises_error(self):
        node = TextNode("Click me!", TextType.LINK)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Link TextNode must have a URL", str(context.exception))

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://www.example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
            "src": "https://www.example.com/image.jpg",
            "alt": "Alt text"
        })

    def test_image_without_url_raises_error(self):
        node = TextNode("Alt text", TextType.IMAGE)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Image TextNode must have a URL", str(context.exception))

    def test_unsupported_text_type_raises_error(self):
        # Create a TextNode with an invalid text_type by directly setting it
        node = TextNode("Some text", TextType.TEXT)
        node.text_type = "INVALID_TYPE"  # Simulate an unsupported type
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Unsupported TextType", str(context.exception))

    def test_text_node_to_html_conversion_end_to_end(self):
        """Test that the converted HTML nodes produce correct HTML output"""
        # Test TEXT
        text_node = TextNode("Just plain text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "Just plain text")

        # Test BOLD
        bold_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(bold_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

        # Test ITALIC
        italic_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(italic_node)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

        # Test CODE
        code_node = TextNode("console.log('hello')", TextType.CODE)
        html_node = text_node_to_html_node(code_node)
        self.assertEqual(html_node.to_html(), "<code>console.log('hello')</code>")

        # Test LINK
        link_node = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(link_node)
        self.assertEqual(html_node.to_html(), '<a href="https://www.boot.dev">Boot.dev</a>')

        # Test IMAGE
        image_node = TextNode("A beautiful sunset", TextType.IMAGE, "https://example.com/sunset.jpg")
        html_node = text_node_to_html_node(image_node)
        self.assertEqual(html_node.to_html(), '<img src="https://example.com/sunset.jpg" alt="A beautiful sunset"></img>')

    def test_empty_text_values(self):
        """Test with empty or minimal text values"""
        # Empty text
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")
        
        # Empty bold
        node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b></b>")


if __name__ == "__main__":
    unittest.main()
