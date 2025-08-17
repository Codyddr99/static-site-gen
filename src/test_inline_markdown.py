import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_code_single_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold_double_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_italic_single_delimiter(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_multiple_delimiters_in_one_node(self):
        node = TextNode("This has `code` and `more code` in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_delimiter_at_start(self):
        node = TextNode("`code` at the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at the beginning", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_delimiter_at_end(self):
        node = TextNode("Text ending with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text ending with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_entire_text_is_delimited(self):
        node = TextNode("`entire text is code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("entire text is code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter_found(self):
        node = TextNode("This text has no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [node]  # Should return the original node unchanged
        self.assertEqual(new_nodes, expected)

    def test_empty_delimiter_content(self):
        node = TextNode("This has `` empty delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode(" empty delimiters", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unmatched_delimiter_raises_error(self):
        node = TextNode("This has `unmatched delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("section not closed", str(context.exception))

    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("First `code` node", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),  # Should pass through unchanged
            TextNode("Second `another code` node", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" node", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),  # Unchanged
            TextNode("Second ", TextType.TEXT),
            TextNode("another code", TextType.CODE),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_text_nodes_pass_through(self):
        nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("Italic text", TextType.ITALIC),
            TextNode("Link text", TextType.LINK, "http://example.com"),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        # Should return exactly the same nodes
        self.assertEqual(new_nodes, nodes)

    def test_consecutive_delimiters(self):
        node = TextNode("Text `first``second` more text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("first", TextType.CODE),
            TextNode("second", TextType.CODE),
            TextNode(" more text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_long_delimiter(self):
        node = TextNode("This is **bold text** in markdown", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" in markdown", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_with_spaces(self):
        node = TextNode("Text with ` spaced code ` block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode(" spaced code ", TextType.CODE),
            TextNode(" block", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [node]  # Empty text should pass through unchanged
        self.assertEqual(new_nodes, expected)

    def test_chain_multiple_split_calls(self):
        """Test that we can chain multiple split_nodes_delimiter calls"""
        # Start with text that has both code and bold
        node = TextNode("This has `code` and **bold** text", TextType.TEXT)
        
        # First split on code
        nodes_after_code = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_after_code = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and **bold** text", TextType.TEXT),
        ]
        self.assertEqual(nodes_after_code, expected_after_code)
        
        # Then split on bold
        final_nodes = split_nodes_delimiter(nodes_after_code, "**", TextType.BOLD)
        expected_final = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(final_nodes, expected_final)


class TestExtractMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_alt(self):
        text = "This has an image with empty alt text ![](https://example.com/image.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com/image.jpg")], matches)

    def test_extract_markdown_images_complex_alt(self):
        text = "![Complex alt text with spaces and symbols!](https://example.com/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("Complex alt text with spaces and symbols!", "https://example.com/image.png")], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_single(self):
        text = "Check out [this awesome site](https://www.example.com)!"
        matches = extract_markdown_links(text)
        self.assertListEqual([("this awesome site", "https://www.example.com")], matches)

    def test_extract_markdown_links_no_links(self):
        text = "This text has no links in it"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty_text(self):
        text = "Link with empty text [](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_markdown_links_complex_text(self):
        text = "A [link with complex text & symbols!](https://example.com/path?param=value)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link with complex text & symbols!", "https://example.com/path?param=value")], matches)

    def test_extract_markdown_mixed_images_and_links(self):
        text = "Here's a ![image](https://img.com/pic.jpg) and a [link](https://example.com)"
        
        # Test that images are found correctly
        images = extract_markdown_images(text)
        self.assertListEqual([("image", "https://img.com/pic.jpg")], images)
        
        # Test that links are found correctly (should not include the image)
        links = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], links)

    def test_extract_markdown_links_not_images(self):
        # Ensure that image syntax is not captured as links
        text = "This has an ![image](https://img.com/pic.jpg) but [this is a link](https://example.com)"
        links = extract_markdown_links(text)
        # Should only find the actual link, not the image
        self.assertListEqual([("this is a link", "https://example.com")], links)

    def test_extract_markdown_images_nested_brackets(self):
        # Test edge cases with brackets in alt text - regex limitation
        text = "![alt [with] brackets](https://example.com)"
        images = extract_markdown_images(text)
        # Due to regex limitations, nested brackets won't match properly
        # The regex stops at the first closing bracket
        self.assertListEqual([], images)

    def test_extract_markdown_links_nested_brackets(self):
        # Test edge cases with brackets in link text - regex limitation
        text = "[link [with] brackets](https://example.com)"
        links = extract_markdown_links(text)
        # Due to regex limitations, nested brackets won't match properly
        # The regex stops at the first closing bracket
        self.assertListEqual([], links)

    def test_extract_markdown_empty_text(self):
        # Test with empty input
        images = extract_markdown_images("")
        links = extract_markdown_links("")
        self.assertListEqual([], images)
        self.assertListEqual([], links)

    def test_extract_markdown_malformed_syntax(self):
        # Test with malformed markdown that shouldn't match
        text = "This has [incomplete and ![incomplete and (incomplete)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertListEqual([], images)
        self.assertListEqual([], links)

    def test_extract_markdown_multiple_on_same_line(self):
        text = "![img1](url1) text [link1](url2) more ![img2](url3) and [link2](url4)"
        
        images = extract_markdown_images(text)
        expected_images = [("img1", "url1"), ("img2", "url3")]
        self.assertListEqual(expected_images, images)
        
        links = extract_markdown_links(text)
        expected_links = [("link1", "url2"), ("link2", "url4")]
        self.assertListEqual(expected_links, links)


class TestSplitNodesImage(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_single(self):
        node = TextNode("Here is an ![awesome image](https://example.com/image.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Here is an ", TextType.TEXT),
            TextNode("awesome image", TextType.IMAGE, "https://example.com/image.jpg"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_at_start(self):
        node = TextNode("![image at start](https://example.com/start.jpg) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image at start", TextType.IMAGE, "https://example.com/start.jpg"),
            TextNode(" followed by text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_at_end(self):
        node = TextNode("Text before ![image at end](https://example.com/end.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("image at end", TextType.IMAGE, "https://example.com/end.jpg"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_entire_text(self):
        node = TextNode("![entire text is image](https://example.com/full.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("entire text is image", TextType.IMAGE, "https://example.com/full.jpg"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_no_images(self):
        node = TextNode("This text has no images at all", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [node]  # Should return original node unchanged
        self.assertListEqual(expected, new_nodes)

    def test_split_images_empty_alt(self):
        node = TextNode("Image with empty alt ![](https://example.com/empty.jpg) text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Image with empty alt ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "https://example.com/empty.jpg"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("First ![img1](url1) node", TextType.TEXT),
            TextNode("Already an image", TextType.IMAGE, "existing.jpg"),  # Should pass through
            TextNode("Second ![img2](url2) node", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" node", TextType.TEXT),
            TextNode("Already an image", TextType.IMAGE, "existing.jpg"),  # Unchanged
            TextNode("Second ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_non_text_nodes_pass_through(self):
        nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("Italic text", TextType.ITALIC),
            TextNode("Link text", TextType.LINK, "http://example.com"),
        ]
        new_nodes = split_nodes_image(nodes)
        # Should return exactly the same nodes
        self.assertListEqual(nodes, new_nodes)

    def test_split_images_consecutive(self):
        node = TextNode("![img1](url1)![img2](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode("img2", TextType.IMAGE, "url2"),
        ]
        self.assertListEqual(expected, new_nodes)


class TestSplitNodesLink(unittest.TestCase):

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_single(self):
        node = TextNode("Check out [this site](https://example.com) for info", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Check out ", TextType.TEXT),
            TextNode("this site", TextType.LINK, "https://example.com"),
            TextNode(" for info", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_at_start(self):
        node = TextNode("[link at start](https://example.com) followed by text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link at start", TextType.LINK, "https://example.com"),
            TextNode(" followed by text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_at_end(self):
        node = TextNode("Text before [link at end](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("link at end", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_entire_text(self):
        node = TextNode("[entire text is link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("entire text is link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_no_links(self):
        node = TextNode("This text has no links at all", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [node]  # Should return original node unchanged
        self.assertListEqual(expected, new_nodes)

    def test_split_links_empty_text(self):
        node = TextNode("Link with empty text [](https://example.com) here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Link with empty text ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://example.com"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("First [link1](url1) node", TextType.TEXT),
            TextNode("Already a link", TextType.LINK, "existing.com"),  # Should pass through
            TextNode("Second [link2](url2) node", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" node", TextType.TEXT),
            TextNode("Already a link", TextType.LINK, "existing.com"),  # Unchanged
            TextNode("Second ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_non_text_nodes_pass_through(self):
        nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("Italic text", TextType.ITALIC),
            TextNode("Image alt", TextType.IMAGE, "http://example.com/img.jpg"),
        ]
        new_nodes = split_nodes_link(nodes)
        # Should return exactly the same nodes
        self.assertListEqual(nodes, new_nodes)

    def test_split_links_consecutive(self):
        node = TextNode("[link1](url1)[link2](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_does_not_match_images(self):
        # Ensure that image syntax is not captured as links
        node = TextNode("This has an ![image](https://img.com/pic.jpg) but [this is a link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This has an ![image](https://img.com/pic.jpg) but ", TextType.TEXT),
            TextNode("this is a link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, new_nodes)


class TestSplitNodesImageAndLink(unittest.TestCase):
    """Test combinations of image and link splitting"""

    def test_split_mixed_images_and_links(self):
        # Test a complex case with both images and links
        node = TextNode(
            "Start ![img](img.jpg) middle [link](link.com) end",
            TextType.TEXT
        )
        
        # First split images
        after_images = split_nodes_image([node])
        expected_after_images = [
            TextNode("Start ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "img.jpg"),
            TextNode(" middle [link](link.com) end", TextType.TEXT),
        ]
        self.assertListEqual(expected_after_images, after_images)
        
        # Then split links
        after_links = split_nodes_link(after_images)
        expected_final = [
            TextNode("Start ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "img.jpg"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("link", TextType.LINK, "link.com"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertListEqual(expected_final, after_links)

    def test_chained_processing_order_matters(self):
        # Test that order of processing matters
        node = TextNode("![image with [link](example.com) in alt](img.jpg)", TextType.TEXT)
        
        # If we split links first, it will find the link inside the image alt text
        after_links_first = split_nodes_link([node])
        # This will split the link even though it's inside image alt text
        expected_after_links = [
            TextNode("![image with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "example.com"),
            TextNode(" in alt](img.jpg)", TextType.TEXT),
        ]
        self.assertListEqual(expected_after_links, after_links_first)
        
        # If we split images first, the regex will match differently due to nested brackets
        after_images_first = split_nodes_image([node])
        # The image regex stops at the first ] after [link, so it matches up to [link only
        expected = [
            TextNode("image with [link", TextType.IMAGE, "example.com"),
            TextNode(" in alt](img.jpg)", TextType.TEXT),
        ]
        self.assertListEqual(expected, after_images_first)


class TestTextToTextNodes(unittest.TestCase):

    def test_text_to_textnodes_example(self):
        # Test the exact example from the requirements
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text with no markdown"
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is just plain text with no markdown", TextType.TEXT)]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_bold(self):
        text = "This is **bold text** only"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" only", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_italic(self):
        text = "This is _italic text_ only"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" only", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_code(self):
        text = "This is `code text` only"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code text", TextType.CODE),
            TextNode(" only", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_image(self):
        text = "This is an ![image](https://example.com/image.jpg) only"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" only", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_link(self):
        text = "This is a [link](https://example.com) only"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" only", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_multiple_same_type(self):
        text = "This has **bold1** and **bold2** and **bold3** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold3", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_nested_not_supported(self):
        # Test that nested markdown is handled as literal text within delimiters
        text = "This is **bold with _italic_ inside** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold with _italic_ inside", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_complex_mixed(self):
        text = "Start **bold** then `code` then _italic_ then ![img](url) then [link](url) end"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" then ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" then ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" then ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" then ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        expected = [TextNode("", TextType.TEXT)]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_whitespace_only(self):
        text = "   \n\t  "
        nodes = text_to_textnodes(text)
        expected = [TextNode("   \n\t  ", TextType.TEXT)]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_consecutive_formatting(self):
        text = "**bold**_italic_`code`![img](url)[link](url)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_formatting_at_boundaries(self):
        # Test formatting at start and end
        text = "**start** middle _end_"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("start", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end", TextType.ITALIC),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_image_and_link_distinction(self):
        # Test that images and links are properly distinguished
        text = "![image](img.jpg) and [link](link.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("image", TextType.IMAGE, "img.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "link.com"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_realistic_markdown(self):
        # Test a more realistic markdown example
        text = "Check out this **awesome** `static site generator` tutorial! It covers _everything_ you need including ![screenshots](https://example.com/screenshot.png) and has a [link to the repo](https://github.com/example/repo)."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Check out this ", TextType.TEXT),
            TextNode("awesome", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("static site generator", TextType.CODE),
            TextNode(" tutorial! It covers ", TextType.TEXT),
            TextNode("everything", TextType.ITALIC),
            TextNode(" you need including ", TextType.TEXT),
            TextNode("screenshots", TextType.IMAGE, "https://example.com/screenshot.png"),
            TextNode(" and has a ", TextType.TEXT),
            TextNode("link to the repo", TextType.LINK, "https://github.com/example/repo"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)


if __name__ == "__main__":
    unittest.main()
