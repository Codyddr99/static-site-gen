def extract_title(markdown):
    """
    Extract the h1 header from markdown text.
    
    Args:
        markdown: Markdown text string
        
    Returns:
        The title text (without the # and whitespace)
        
    Raises:
        Exception: If no h1 header is found
        
    Example:
        extract_title("# Hello World") -> "Hello World"
    """
    lines = markdown.split('\n')
    
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('#') and (len(stripped_line) == 1 or stripped_line[1] == ' ' or stripped_line[1:].isspace()):
            # Extract the title by removing the '#' and any following whitespace
            if len(stripped_line) == 1:
                return ""
            else:
                title = stripped_line[1:].strip()
                return title
    
    # If we get here, no h1 header was found
    raise Exception("No h1 header found in markdown")


if __name__ == "__main__":
    # Test the function
    test1 = "# Hello World"
    print(f"Test 1: {repr(test1)} -> {repr(extract_title(test1))}")
    
    test2 = """
Some content here

# My Title

More content
"""
    print(f"Test 2: {repr(test2)} -> {repr(extract_title(test2))}")
    
    test3 = "## Not an h1\n### Also not an h1"
    try:
        extract_title(test3)
    except Exception as e:
        print(f"Test 3: {repr(test3)} -> Exception: {e}")
