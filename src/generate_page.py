import os
from extract_title import extract_title
from block_markdown import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from a markdown file using a template.
    
    Args:
        from_path: Path to the markdown file
        template_path: Path to the HTML template file  
        dest_path: Path where the generated HTML should be written
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the final HTML to the destination file
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Page generated successfully at {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generate HTML pages from all markdown files in a directory.
    
    Args:
        dir_path_content: Path to the content directory containing markdown files
        template_path: Path to the HTML template file
        dest_dir_path: Path to the destination directory for generated HTML files
    """
    print(f"Generating pages recursively from {dir_path_content} to {dest_dir_path}")
    
    # Walk through all directories and files in the content directory
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                # Get the full path to the markdown file
                markdown_path = os.path.join(root, file)
                
                # Calculate the relative path from the content directory
                rel_path = os.path.relpath(markdown_path, dir_path_content)
                
                # Change the extension from .md to .html
                html_rel_path = rel_path.replace('.md', '.html')
                
                # Create the destination path
                dest_path = os.path.join(dest_dir_path, html_rel_path)
                
                # Generate the page
                generate_page(markdown_path, template_path, dest_path)
    
    print(f"Finished generating all pages from {dir_path_content}")


if __name__ == "__main__":
    # Test the functions
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    dest_dir = os.path.join(project_root, "public")
    
    print("Testing generate_pages_recursive function:")
    generate_pages_recursive(content_dir, template_path, dest_dir)
