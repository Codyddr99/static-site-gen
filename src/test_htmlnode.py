import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_with_attributes(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "id": "hello"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" id="hello"',
        )

    def test_props_to_html_with_no_attributes(self):
        node = HTMLNode("div", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_single_attribute(self):
        node = HTMLNode(
            "a",
            "Click me!",
            None,
            {"href": "https://www.google.com"}
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com"',
        )

    def test_props_to_html_with_multiple_attributes(self):
        node = HTMLNode(
            "a",
            "Click me!",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_to_html_no_children(self):
        node = HTMLNode("p", "Hello, world!")
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
