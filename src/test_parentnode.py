import unittest
from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span>child</span></div>'
        )

    def test_to_html_nested_parents(self):
        # Deep nesting: div > p > span > b
        innermost = LeafNode("b", "bold text")
        span_node = ParentNode("span", [innermost])
        p_node = ParentNode("p", [span_node])
        div_node = ParentNode("div", [p_node])
        self.assertEqual(
            div_node.to_html(),
            "<div><p><span><b>bold text</b></span></p></div>"
        )

    def test_to_html_mixed_children(self):
        # Mix of LeafNodes and ParentNodes as children
        leaf1 = LeafNode("b", "Bold")
        leaf2 = LeafNode(None, " and ")
        parent_child = ParentNode("em", [LeafNode(None, "emphasized")])
        leaf3 = LeafNode(None, " text")
        
        parent = ParentNode("p", [leaf1, leaf2, parent_child, leaf3])
        self.assertEqual(
            parent.to_html(),
            "<p><b>Bold</b> and <em>emphasized</em> text</p>"
        )

    def test_to_html_no_tag_raises_error(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("no tag", str(context.exception))

    def test_to_html_no_children_raises_error(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("no children", str(context.exception))

    def test_to_html_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_single_child(self):
        child = LeafNode("span", "single child")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span>single child</span></div>")

    def test_to_html_complex_nesting(self):
        # Create a more complex structure
        # <article>
        #   <h1>Title</h1>
        #   <p>Some <b>bold</b> and <i>italic</i> text.</p>
        #   <div><span>Nested content</span></div>
        # </article>
        
        title = LeafNode("h1", "Title")
        
        p_content = ParentNode("p", [
            LeafNode(None, "Some "),
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
            LeafNode(None, " text.")
        ])
        
        nested_div = ParentNode("div", [
            LeafNode("span", "Nested content")
        ])
        
        article = ParentNode("article", [title, p_content, nested_div])
        
        expected = "<article><h1>Title</h1><p>Some <b>bold</b> and <i>italic</i> text.</p><div><span>Nested content</span></div></article>"
        self.assertEqual(article.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
