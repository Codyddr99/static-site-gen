import unittest
from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is just raw text.")
        self.assertEqual(node.to_html(), "This is just raw text.")

    def test_leaf_to_html_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "This is a heading")
        self.assertEqual(node.to_html(), "<h1>This is a heading</h1>")

    def test_leaf_to_html_img_with_props(self):
        node = LeafNode("img", "", {"src": "image.jpg", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="An image"></img>')

    def test_leaf_to_html_span_with_multiple_props(self):
        node = LeafNode("span", "Styled text", {"class": "highlight", "id": "special"})
        self.assertEqual(node.to_html(), '<span class="highlight" id="special">Styled text</span>')

    def test_leaf_to_html_br_empty_value(self):
        node = LeafNode("br", "")
        self.assertEqual(node.to_html(), "<br></br>")


if __name__ == "__main__":
    unittest.main()
