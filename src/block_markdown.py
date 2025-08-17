import re
from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType
from text_to_html import text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    
    Args:
        block: A single block of markdown text (whitespace already stripped)
        
    Returns:
        BlockType enum representing the type of block
    """
    lines = block.split("\n")
    
    # Check for heading (1-6 # characters followed by space)
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    
    # Check for code block (starts and ends with 3 backticks)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Check for quote block (every line starts with >)
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with - followed by space)
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (lines start with number. followed by space, incrementing from 1)
    if len(lines) > 0:
        expected_num = 1
        is_ordered_list = True
        for line in lines:
            if not re.match(rf"^{expected_num}\. ", line):
                is_ordered_list = False
                break
            expected_num += 1
        if is_ordered_list:
            return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    """
    Split a markdown string into a list of block strings.
    
    Blocks are separated by double newlines (\n\n). Each block is stripped of
    leading/trailing whitespace, and empty blocks are removed.
    
    Args:
        markdown: Raw markdown string representing a full document
        
    Returns:
        List of block strings
        
    Example:
        markdown_to_blocks("# Heading\n\nParagraph text")
        -> ["# Heading", "Paragraph text"]
    """
    # Split on double newlines to get blocks
    blocks = markdown.split("\n\n")
    
    # Strip whitespace from each block and filter out empty blocks
    filtered_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:  # Only add non-empty blocks
            filtered_blocks.append(stripped_block)
    
    return filtered_blocks


def text_to_children(text):
    """
    Convert inline markdown text to a list of HTMLNode children.
    
    This is a shared helper function that converts text with inline markdown
    (bold, italic, code, links, images) into HTMLNode objects.
    
    Args:
        text: String containing inline markdown
        
    Returns:
        List of HTMLNode objects representing the inline elements
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def heading_to_html_node(block):
    """Convert a heading block to an HTMLNode."""
    # Count the number of # characters
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    
    # Extract the heading text (skip the # and space)
    heading_text = block[level + 1:]
    
    # Create the heading tag
    tag = f"h{level}"
    children = text_to_children(heading_text)
    
    return ParentNode(tag, children)


def paragraph_to_html_node(block):
    """Convert a paragraph block to an HTMLNode."""
    # Replace single newlines with spaces for paragraph text
    text = block.replace("\n", " ")
    children = text_to_children(text)
    return ParentNode("p", children)


def code_to_html_node(block):
    """Convert a code block to an HTMLNode."""
    # Remove the opening and closing backticks
    code_text = block[3:-3]  # Remove ``` from start and end
    
    # Strip leading newline if it exists (common in markdown code blocks)
    if code_text.startswith("\n"):
        code_text = code_text[1:]
    
    # Code blocks should not process inline markdown
    # Create a single text node and convert to HTML
    text_node = TextNode(code_text, TextType.TEXT)
    code_leaf = text_node_to_html_node(text_node)
    
    # Wrap in <code> tag, then in <pre> tag
    code_node = ParentNode("code", [code_leaf])
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    """Convert a quote block to an HTMLNode."""
    # Remove the > from each line and join with newlines
    lines = block.split("\n")
    quote_lines = []
    for line in lines:
        # Remove the > and any space after it
        if line.startswith("> "):
            quote_lines.append(line[2:])
        elif line.startswith(">"):
            quote_lines.append(line[1:])
        else:
            quote_lines.append(line)
    
    # Join lines back together with newlines, then convert to spaces for inline processing
    quote_text = "\n".join(quote_lines).replace("\n", " ")
    children = text_to_children(quote_text)
    
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """Convert an unordered list block to an HTMLNode."""
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        # Remove the "- " from the beginning
        item_text = line[2:]
        children = text_to_children(item_text)
        list_item = ParentNode("li", children)
        list_items.append(list_item)
    
    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    """Convert an ordered list block to an HTMLNode."""
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        # Remove the number and ". " from the beginning
        # Find the first ". " and remove everything up to and including it
        dot_index = line.find(". ")
        item_text = line[dot_index + 2:]
        children = text_to_children(item_text)
        list_item = ParentNode("li", children)
        list_items.append(list_item)
    
    return ParentNode("ol", list_items)


def markdown_to_html_node(markdown):
    """
    Convert a full markdown document into a single parent HTMLNode.
    
    Args:
        markdown: Full markdown document string
        
    Returns:
        ParentNode representing the entire document as a div containing all blocks
    """
    # Split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # Convert each block to HTML nodes
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.HEADING:
            html_node = heading_to_html_node(block)
        elif block_type == BlockType.PARAGRAPH:
            html_node = paragraph_to_html_node(block)
        elif block_type == BlockType.CODE:
            html_node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            html_node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            html_node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            html_node = ordered_list_to_html_node(block)
        else:
            # Default to paragraph
            html_node = paragraph_to_html_node(block)
        
        block_nodes.append(html_node)
    
    # Wrap all blocks in a div
    return ParentNode("div", block_nodes)
