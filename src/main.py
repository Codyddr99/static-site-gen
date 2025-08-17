from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_html import text_node_to_html_node
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
from copy_static import copy_files_recursive
from generate_page import generate_page, generate_pages_recursive
import os

def main():
    print("="*60)
    print("STATIC SITE GENERATOR")
    print("="*60)
    
    # Get project paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    source_static = os.path.join(current_dir, "static")
    dest_public = os.path.join(project_root, "public")
    
    # Step 1: Copy static files to public directory
    print("\n--- Step 1: Copying static files ---")
    copy_files_recursive(source_static, dest_public)
    
    # Step 2: Generate all pages from content directory
    print("\n--- Step 2: Generating all pages ---")
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    
    generate_pages_recursive(content_dir, template_path, dest_public)
    
    print("\n--- Static site generation complete! ---")
    print(f"Website generated in: {dest_public}")
    print("You can now serve the site with: cd public && python3 -m http.server 8888")
    
    print("\n--- Testing TextNode and HTMLNode functionality ---")
    
    # Create a TextNode with dummy values
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    
    # Test HTMLNode
    html_node = HTMLNode("div", "Hello, world!", None, {"class": "greeting", "id": "hello"})
    print(html_node)
    print("Props to HTML:", html_node.props_to_html())
    
    # Test LeafNode
    leaf_node = LeafNode("p", "This is a paragraph of text.")
    print("Leaf node:", leaf_node)
    print("Leaf to HTML:", leaf_node.to_html())
    
    # Test LeafNode with props
    link_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print("Link node:", link_node)
    print("Link to HTML:", link_node.to_html())
    
    # Test raw text (no tag)
    raw_text_node = LeafNode(None, "Just some raw text")
    print("Raw text node:", raw_text_node)
    print("Raw text to HTML:", raw_text_node.to_html())
    
    # Test ParentNode
    parent_node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    print("Parent node:", parent_node)
    print("Parent to HTML:", parent_node.to_html())
    
    # Test nested ParentNode
    nested_parent = ParentNode(
        "div",
        [
            LeafNode("h1", "Heading"),
            parent_node,  # Nest the previous parent
            LeafNode("span", "Footer text")
        ],
        {"class": "container"}
    )
    print("Nested parent:", nested_parent)
    print("Nested parent to HTML:", nested_parent.to_html())
    
    # Test text_node_to_html_node function
    print("\n--- Testing text_node_to_html_node ---")
    
    # Test all TextType conversions
    text_node = TextNode("Plain text", TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    print(f"TEXT: {text_node} -> {html_node.to_html()}")
    
    bold_node = TextNode("Bold text", TextType.BOLD)
    html_node = text_node_to_html_node(bold_node)
    print(f"BOLD: {bold_node} -> {html_node.to_html()}")
    
    italic_node = TextNode("Italic text", TextType.ITALIC)
    html_node = text_node_to_html_node(italic_node)
    print(f"ITALIC: {italic_node} -> {html_node.to_html()}")
    
    code_node = TextNode("print('hello')", TextType.CODE)
    html_node = text_node_to_html_node(code_node)
    print(f"CODE: {code_node} -> {html_node.to_html()}")
    
    link_node = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
    html_node = text_node_to_html_node(link_node)
    print(f"LINK: {link_node} -> {html_node.to_html()}")
    
    image_node = TextNode("A cool image", TextType.IMAGE, "https://example.com/image.jpg")
    html_node = text_node_to_html_node(image_node)
    print(f"IMAGE: {image_node} -> {html_node.to_html()}")
    
    # Test split_nodes_delimiter function
    print("\n--- Testing split_nodes_delimiter ---")
    
    # Test code delimiter
    original_node = TextNode("This is text with a `code block` word", TextType.TEXT)
    print(f"Original: {original_node}")
    split_nodes = split_nodes_delimiter([original_node], "`", TextType.CODE)
    print("After splitting on backticks:")
    for i, node in enumerate(split_nodes):
        print(f"  {i}: {node}")
    
    # Test bold delimiter
    bold_text_node = TextNode("This is **bold** text with **more bold** words", TextType.TEXT)
    print(f"\nOriginal: {bold_text_node}")
    bold_split = split_nodes_delimiter([bold_text_node], "**", TextType.BOLD)
    print("After splitting on **:")
    for i, node in enumerate(bold_split):
        print(f"  {i}: {node}")
    
    # Test italic delimiter
    italic_text_node = TextNode("This is _italic_ text", TextType.TEXT)
    print(f"\nOriginal: {italic_text_node}")
    italic_split = split_nodes_delimiter([italic_text_node], "_", TextType.ITALIC)
    print("After splitting on _:")
    for i, node in enumerate(italic_split):
        print(f"  {i}: {node}")
    
    # Test chaining multiple splits
    print("\n--- Testing chained splits ---")
    complex_node = TextNode("This has `code` and **bold** and _italic_ text", TextType.TEXT)
    print(f"Original: {complex_node}")
    
    # Split on code first
    after_code = split_nodes_delimiter([complex_node], "`", TextType.CODE)
    print("After code split:")
    for i, node in enumerate(after_code):
        print(f"  {i}: {node}")
    
    # Then split on bold
    after_bold = split_nodes_delimiter(after_code, "**", TextType.BOLD)
    print("After bold split:")
    for i, node in enumerate(after_bold):
        print(f"  {i}: {node}")
    
    # Finally split on italic
    final_nodes = split_nodes_delimiter(after_bold, "_", TextType.ITALIC)
    print("After italic split:")
    for i, node in enumerate(final_nodes):
        print(f"  {i}: {node}")
    
    # Convert final nodes to HTML to see the result
    print("\nFinal HTML output:")
    html_nodes = [text_node_to_html_node(node) for node in final_nodes]
    html_output = "".join(node.to_html() for node in html_nodes)
    print(f"HTML: {html_output}")
    
    # Test extract_markdown_images function
    print("\n--- Testing extract_markdown_images ---")
    
    image_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(f"Text: {image_text}")
    images = extract_markdown_images(image_text)
    print(f"Extracted images: {images}")
    
    single_image_text = "Here's an ![awesome image](https://example.com/cool.png) in the text"
    print(f"\nText: {single_image_text}")
    single_image = extract_markdown_images(single_image_text)
    print(f"Extracted images: {single_image}")
    
    no_image_text = "This text has no images at all"
    print(f"\nText: {no_image_text}")
    no_images = extract_markdown_images(no_image_text)
    print(f"Extracted images: {no_images}")
    
    # Test extract_markdown_links function
    print("\n--- Testing extract_markdown_links ---")
    
    link_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(f"Text: {link_text}")
    links = extract_markdown_links(link_text)
    print(f"Extracted links: {links}")
    
    single_link_text = "Check out [this awesome site](https://www.example.com) for more info"
    print(f"\nText: {single_link_text}")
    single_link = extract_markdown_links(single_link_text)
    print(f"Extracted links: {single_link}")
    
    no_link_text = "This text has no links whatsoever"
    print(f"\nText: {no_link_text}")
    no_links = extract_markdown_links(no_link_text)
    print(f"Extracted links: {no_links}")
    
    # Test mixed images and links
    print("\n--- Testing mixed images and links ---")
    
    mixed_text = "Here's an ![image](https://img.com/pic.jpg) and a [link](https://example.com) in the same text"
    print(f"Text: {mixed_text}")
    mixed_images = extract_markdown_images(mixed_text)
    mixed_links = extract_markdown_links(mixed_text)
    print(f"Extracted images: {mixed_images}")
    print(f"Extracted links: {mixed_links}")
    
    # Demonstrate that images are not captured as links
    image_only_text = "This text has only an ![image](https://img.com/test.jpg) and no links"
    print(f"\nText: {image_only_text}")
    image_as_link = extract_markdown_links(image_only_text)
    print(f"Links found (should be empty): {image_as_link}")
    
    # Test split_nodes_image function
    print("\n--- Testing split_nodes_image ---")
    
    image_node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    print(f"Original: {image_node}")
    split_image_nodes = split_nodes_image([image_node])
    print("After splitting images:")
    for i, node in enumerate(split_image_nodes):
        print(f"  {i}: {node}")
    
    # Test single image
    single_image_node = TextNode("Here is an ![awesome image](https://example.com/image.jpg)", TextType.TEXT)
    print(f"\nOriginal: {single_image_node}")
    single_split = split_nodes_image([single_image_node])
    print("After splitting:")
    for i, node in enumerate(single_split):
        print(f"  {i}: {node}")
    
    # Test split_nodes_link function
    print("\n--- Testing split_nodes_link ---")
    
    link_node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    print(f"Original: {link_node}")
    split_link_nodes = split_nodes_link([link_node])
    print("After splitting links:")
    for i, node in enumerate(split_link_nodes):
        print(f"  {i}: {node}")
    
    # Test single link
    single_link_node = TextNode("Check out [this site](https://example.com) for info", TextType.TEXT)
    print(f"\nOriginal: {single_link_node}")
    single_link_split = split_nodes_link([single_link_node])
    print("After splitting:")
    for i, node in enumerate(single_link_split):
        print(f"  {i}: {node}")
    
    # Test comprehensive markdown processing pipeline
    print("\n--- Testing complete markdown processing pipeline ---")
    
    complex_markdown = TextNode(
        "This has `code`, **bold**, _italic_, ![image](img.jpg), and [link](example.com) all together!",
        TextType.TEXT,
    )
    print(f"Original: {complex_markdown}")
    
    # Step 1: Split delimiters (code, bold, italic)
    step1 = split_nodes_delimiter([complex_markdown], "`", TextType.CODE)
    step2 = split_nodes_delimiter(step1, "**", TextType.BOLD)
    step3 = split_nodes_delimiter(step2, "_", TextType.ITALIC)
    
    print("After delimiter splits:")
    for i, node in enumerate(step3):
        print(f"  {i}: {node}")
    
    # Step 2: Split images
    step4 = split_nodes_image(step3)
    print("After image split:")
    for i, node in enumerate(step4):
        print(f"  {i}: {node}")
    
    # Step 3: Split links
    final_step = split_nodes_link(step4)
    print("After link split (final):")
    for i, node in enumerate(final_step):
        print(f"  {i}: {node}")
    
    # Convert to HTML to see the final result
    print("\nFinal HTML output:")
    final_html_nodes = [text_node_to_html_node(node) for node in final_step]
    final_html = "".join(node.to_html() for node in final_html_nodes)
    print(f"HTML: {final_html}")
    
    # Test mixed images and links
    print("\n--- Testing mixed images and links ---")
    
    mixed_node = TextNode(
        "Start ![img](img.jpg) middle [link](link.com) end",
        TextType.TEXT
    )
    print(f"Original: {mixed_node}")
    
    # Process images first, then links
    after_images = split_nodes_image([mixed_node])
    print("After splitting images:")
    for i, node in enumerate(after_images):
        print(f"  {i}: {node}")
    
    after_both = split_nodes_link(after_images)
    print("After splitting links:")
    for i, node in enumerate(after_both):
        print(f"  {i}: {node}")
    
    # Convert to HTML
    mixed_html_nodes = [text_node_to_html_node(node) for node in after_both]
    mixed_html = "".join(node.to_html() for node in mixed_html_nodes)
    print(f"Final HTML: {mixed_html}")
    
    # Test text_to_textnodes function (the complete pipeline)
    print("\n--- Testing text_to_textnodes (Complete Pipeline) ---")
    
    # Test the exact example from the requirements
    example_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(f"Input text: {example_text}")
    
    parsed_nodes = text_to_textnodes(example_text)
    print("Parsed nodes:")
    for i, node in enumerate(parsed_nodes):
        print(f"  {i}: {node}")
    
    # Convert to HTML to see the final result
    html_nodes = [text_node_to_html_node(node) for node in parsed_nodes]
    final_html = "".join(node.to_html() for node in html_nodes)
    print(f"Final HTML: {final_html}")
    
    # Test with simpler examples
    print("\n--- Testing simpler examples ---")
    
    simple_examples = [
        "Just plain text",
        "This is **bold** text",
        "This is _italic_ text", 
        "This is `code` text",
        "This is an ![image](https://example.com/img.jpg)",
        "This is a [link](https://example.com)",
        "**bold** and _italic_ together",
        "`code` with **bold** mixed",
        "![img](url) and [link](url) together"
    ]
    
    for example in simple_examples:
        print(f"\nInput: {example}")
        nodes = text_to_textnodes(example)
        print("Nodes:")
        for i, node in enumerate(nodes):
            print(f"  {i}: {node}")
        
        # Convert to HTML
        html_nodes = [text_node_to_html_node(node) for node in nodes]
        html_output = "".join(node.to_html() for node in html_nodes)
        print(f"HTML: {html_output}")
    
    # Test a realistic markdown example
    print("\n--- Testing realistic markdown ---")
    realistic_text = "Check out this **awesome** `static site generator` tutorial! It covers _everything_ you need including ![screenshots](https://example.com/screenshot.png) and has a [link to the repo](https://github.com/example/repo)."
    print(f"Input: {realistic_text}")
    
    realistic_nodes = text_to_textnodes(realistic_text)
    print("Parsed nodes:")
    for i, node in enumerate(realistic_nodes):
        print(f"  {i}: {node}")
    
    # Convert to HTML
    realistic_html_nodes = [text_node_to_html_node(node) for node in realistic_nodes]
    realistic_html = "".join(node.to_html() for node in realistic_html_nodes)
    print(f"Final HTML: {realistic_html}")
    
    # Test markdown_to_blocks function
    print("\n--- Testing markdown_to_blocks ---")
    
    # Test the example from requirements
    example_markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    print("Input markdown:")
    print(repr(example_markdown))
    
    blocks = markdown_to_blocks(example_markdown)
    print("\nBlocks:")
    for i, block in enumerate(blocks):
        print(f"  {i}: {repr(block)}")
    
    # Test a more complex example
    complex_markdown = """# Main Heading

This is a paragraph with some **bold** text and _italic_ text.

## Subheading

Another paragraph here.

- First list item
- Second list item
- Third list item

> This is a blockquote
> with multiple lines

```
code block
with multiple lines
```

Final paragraph at the end."""
    
    print(f"\n--- Testing complex markdown ---")
    print("Input:")
    print(complex_markdown)
    
    complex_blocks = markdown_to_blocks(complex_markdown)
    print("\nBlocks:")
    for i, block in enumerate(complex_blocks):
        print(f"  {i}: {repr(block)}")
    
    # Test edge cases
    print(f"\n--- Testing edge cases ---")
    
    # Excessive newlines
    excessive_newlines = """# Heading



Paragraph with excessive newlines



- List item


Final text"""
    
    print("Excessive newlines test:")
    excessive_blocks = markdown_to_blocks(excessive_newlines)
    for i, block in enumerate(excessive_blocks):
        print(f"  {i}: {repr(block)}")
    
    # Whitespace handling
    whitespace_test = """   # Heading with spaces   

  Paragraph with leading/trailing spaces  

- List item  """
    
    print("\nWhitespace handling test:")
    whitespace_blocks = markdown_to_blocks(whitespace_test)
    for i, block in enumerate(whitespace_blocks):
        print(f"  {i}: {repr(block)}")
    
    # Demonstrate the complete pipeline: markdown -> blocks -> textnodes -> HTML
    print(f"\n--- Complete pipeline demonstration ---")
    simple_md = """# Welcome

This is a **bold** statement with _italic_ text and `code`.

- Item 1
- Item 2"""
    
    print("Original markdown:")
    print(simple_md)
    
    # Step 1: Split into blocks
    md_blocks = markdown_to_blocks(simple_md)
    print("\nStep 1 - Blocks:")
    for i, block in enumerate(md_blocks):
        print(f"  {i}: {repr(block)}")
    
    # Step 2: Convert each block to textnodes (just for the paragraph block)
    print("\nStep 2 - Converting paragraph block to textnodes:")
    paragraph_block = md_blocks[1]  # The paragraph with formatting
    paragraph_nodes = text_to_textnodes(paragraph_block)
    for i, node in enumerate(paragraph_nodes):
        print(f"  {i}: {node}")
    
    # Step 3: Convert to HTML
    print("\nStep 3 - Converting to HTML:")
    paragraph_html_nodes = [text_node_to_html_node(node) for node in paragraph_nodes]
    paragraph_html = "".join(node.to_html() for node in paragraph_html_nodes)
    print(f"Paragraph HTML: {paragraph_html}")
    
    print("\n" + "="*60)
    print("NEW: BLOCK TYPE DETECTION")
    print("="*60)
    
    # Demonstrate block type detection
    test_blocks = [
        "# This is a heading",
        "## Another heading with **bold** text",
        "This is just a paragraph with some text.",
        "> This is a quote block\n> with multiple lines",
        "- First list item\n- Second list item\n- Third list item",
        "1. First ordered item\n2. Second ordered item\n3. Third ordered item",
        "```\nprint('This is code')\nreturn True\n```"
    ]
    
    for i, block in enumerate(test_blocks):
        block_type = block_to_block_type(block)
        print(f"\nBlock {i+1}: {block_type}")
        print(f"Content: {repr(block)}")
    
    print("\n" + "="*60)
    print("NEW: COMPLETE MARKDOWN TO HTML CONVERSION")
    print("="*60)
    
    # Demonstrate complete markdown to HTML conversion
    full_markdown = """# My Blog Post

This is a **bold** introduction paragraph with some _italic_ text and `inline code`.

## Section 1: Lists

Here's an unordered list:

- First item with **bold** text
- Second item with [a link](https://example.com)
- Third item with `code`

And here's an ordered list:

1. Step one
2. Step two with _emphasis_
3. Step three

## Section 2: Code and Quotes

Here's a code block:

```python
def hello_world():
    print("Hello, world!")
    return True
```

And here's a quote:

> This is a quote from someone famous.
> It spans multiple lines.

That's the end of my blog post!"""

    print("Converting full markdown document to HTML...")
    html_node = markdown_to_html_node(full_markdown)
    html_output = html_node.to_html()
    
    print(f"\nFull HTML output:")
    print(html_output)
    
    # Pretty print the HTML with some formatting
    print(f"\nFormatted HTML structure:")
    formatted_html = html_output.replace("><", ">\n<")
    print(formatted_html)

if __name__ == "__main__":
    main()