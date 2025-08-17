import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split TextNode objects based on a delimiter, converting delimited text to a specific text type.
    
    Args:
        old_nodes: List of TextNode objects to process
        delimiter: String delimiter to split on (e.g., "`", "**", "_")
        text_type: TextType to assign to text found between delimiters
        
    Returns:
        List of TextNode objects with delimited sections converted to the specified text_type
        
    Raises:
        ValueError: If a delimiter is not properly closed (unmatched delimiter)
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only split TEXT type nodes, pass through others unchanged
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Split the text by the delimiter
        split_nodes = []
        sections = old_node.text.split(delimiter)
        
        # If there's only one section, no delimiter was found
        if len(sections) == 1:
            new_nodes.append(old_node)
            continue
            
        # Check for unmatched delimiters (odd number of sections means unclosed delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid markdown, {delimiter} section not closed")
            
        for i, section in enumerate(sections):
            # Skip empty sections (happens when delimiter is at start/end or consecutive delimiters)
            if section == "":
                continue
                
            if i % 2 == 0:
                # Even indices are regular text (outside delimiters)
                split_nodes.append(TextNode(section, TextType.TEXT))
            else:
                # Odd indices are delimited text (inside delimiters)
                split_nodes.append(TextNode(section, text_type))
        
        new_nodes.extend(split_nodes)
    
    return new_nodes


def extract_markdown_images(text):
    """
    Extract markdown images from text.
    
    Args:
        text: String containing markdown text
        
    Returns:
        List of tuples (alt_text, url) for each image found
        
    Example:
        extract_markdown_images("![alt](url)") -> [("alt", "url")]
    """
    # Regex pattern for markdown images: ![alt text](url)
    # Match non-greedy up to closing brackets, but handle nested brackets better
    pattern = r"!\[([^\]]*)\]\(([^\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    """
    Extract markdown links from text.
    
    Args:
        text: String containing markdown text
        
    Returns:
        List of tuples (anchor_text, url) for each link found
        
    Example:
        extract_markdown_links("[text](url)") -> [("text", "url")]
    """
    # Regex pattern for markdown links: [anchor text](url)
    # This pattern should not match images (which start with !)
    # Match non-greedy up to closing brackets, but handle nested brackets better
    pattern = r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    """
    Split TextNode objects on markdown images, converting image syntax to IMAGE type nodes.
    
    Args:
        old_nodes: List of TextNode objects to process
        
    Returns:
        List of TextNode objects with image syntax converted to IMAGE nodes
        
    Example:
        Input: [TextNode("Text ![alt](url) more", TextType.TEXT)]
        Output: [TextNode("Text ", TextType.TEXT), 
                TextNode("alt", TextType.IMAGE, "url"), 
                TextNode(" more", TextType.TEXT)]
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only split TEXT type nodes, pass through others unchanged
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Extract all images from the text
        images = extract_markdown_images(old_node.text)
        
        # If no images found, keep the original node
        if not images:
            new_nodes.append(old_node)
            continue
            
        # Split the text based on image positions
        current_text = old_node.text
        
        for alt_text, url in images:
            # Find the full image markdown syntax in the text
            image_markdown = f"![{alt_text}]({url})"
            
            # Split on this specific image
            parts = current_text.split(image_markdown, 1)  # Split only on first occurrence
            
            if len(parts) == 2:
                # Add the text before the image (if not empty)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
                # Add the image node
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                
                # Continue with the remaining text
                current_text = parts[1]
        
        # Add any remaining text after the last image
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split TextNode objects on markdown links, converting link syntax to LINK type nodes.
    
    Args:
        old_nodes: List of TextNode objects to process
        
    Returns:
        List of TextNode objects with link syntax converted to LINK nodes
        
    Example:
        Input: [TextNode("Text [anchor](url) more", TextType.TEXT)]
        Output: [TextNode("Text ", TextType.TEXT), 
                TextNode("anchor", TextType.LINK, "url"), 
                TextNode(" more", TextType.TEXT)]
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only split TEXT type nodes, pass through others unchanged
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Extract all links from the text
        links = extract_markdown_links(old_node.text)
        
        # If no links found, keep the original node
        if not links:
            new_nodes.append(old_node)
            continue
            
        # Split the text based on link positions
        current_text = old_node.text
        
        for anchor_text, url in links:
            # Find the full link markdown syntax in the text
            link_markdown = f"[{anchor_text}]({url})"
            
            # Split on this specific link
            parts = current_text.split(link_markdown, 1)  # Split only on first occurrence
            
            if len(parts) == 2:
                # Add the text before the link (if not empty)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
                # Add the link node
                new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                
                # Continue with the remaining text
                current_text = parts[1]
        
        # Add any remaining text after the last link
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes


def text_to_textnodes(text):
    """
    Convert raw markdown text to a list of TextNode objects.
    
    This function applies all the inline markdown parsing in the correct order:
    1. Split on code delimiters (`)
    2. Split on bold delimiters (**)
    3. Split on italic delimiters (_)
    4. Split on images (![alt](url))
    5. Split on links ([anchor](url))
    
    Args:
        text: Raw markdown text string
        
    Returns:
        List of TextNode objects representing the parsed text
        
    Example:
        text_to_textnodes("**bold** and `code`")
        -> [TextNode("bold", TextType.BOLD), TextNode(" and ", TextType.TEXT), 
            TextNode("code", TextType.CODE)]
    """
    # Start with a single TEXT node containing all the text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Apply all the splitting functions in order
    # Order matters: delimiters first, then images, then links
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes
