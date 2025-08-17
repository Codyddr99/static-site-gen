import unittest
import os
import tempfile
import shutil
from generate_page import generate_page, generate_pages_recursive
from extract_title import extract_title


class TestGeneratePage(unittest.TestCase):
    
    def setUp(self):
        """Set up temporary directories and files for testing."""
        self.test_dir = tempfile.mkdtemp()
        
        # Create test markdown content
        self.markdown_content = """# Test Page

This is a **test** page with some content.

## Section 1

- Item 1
- Item 2

> This is a quote.

```
code block
```
"""
        
        # Create test template
        self.template_content = """<!DOCTYPE html>
<html>
<head>
    <title>{{ Title }}</title>
</head>
<body>
    <h1>{{ Title }}</h1>
    <div>{{ Content }}</div>
</body>
</html>"""
        
        # Write test files
        self.markdown_path = os.path.join(self.test_dir, "test.md")
        self.template_path = os.path.join(self.test_dir, "template.html")
        self.output_path = os.path.join(self.test_dir, "output.html")
        
        with open(self.markdown_path, 'w') as f:
            f.write(self.markdown_content)
        
        with open(self.template_path, 'w') as f:
            f.write(self.template_content)
    
    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.test_dir)
    
    def test_generate_page_creates_html_file(self):
        """Test that generate_page creates an HTML file."""
        generate_page(self.markdown_path, self.template_path, self.output_path)
        self.assertTrue(os.path.exists(self.output_path))
    
    def test_generate_page_replaces_title(self):
        """Test that the title placeholder is replaced correctly."""
        generate_page(self.markdown_path, self.template_path, self.output_path)
        
        with open(self.output_path, 'r') as f:
            content = f.read()
        
        self.assertIn("<title>Test Page</title>", content)
        self.assertIn("<h1>Test Page</h1>", content)
        self.assertNotIn("{{ Title }}", content)
    
    def test_generate_page_replaces_content(self):
        """Test that the content placeholder is replaced correctly."""
        generate_page(self.markdown_path, self.template_path, self.output_path)
        
        with open(self.output_path, 'r') as f:
            content = f.read()
        
        # Check for converted markdown elements
        self.assertIn("<b>test</b>", content)  # **test** -> <b>test</b>
        self.assertIn("<h2>Section 1</h2>", content)
        self.assertIn("<ul>", content)
        self.assertIn("<li>Item 1</li>", content)
        self.assertIn("<blockquote>", content)
        self.assertIn("<pre><code>", content)
        self.assertNotIn("{{ Content }}", content)
    
    def test_generate_page_creates_directories(self):
        """Test that generate_page creates necessary directories."""
        nested_output = os.path.join(self.test_dir, "nested", "dir", "output.html")
        generate_page(self.markdown_path, self.template_path, nested_output)
        
        self.assertTrue(os.path.exists(nested_output))
        self.assertTrue(os.path.exists(os.path.dirname(nested_output)))
    
    def test_generate_pages_recursive_creates_all_pages(self):
        """Test that generate_pages_recursive creates all pages."""
        # Create content directory structure
        content_dir = os.path.join(self.test_dir, "content")
        os.makedirs(content_dir)
        
        # Create main index.md
        index_md = os.path.join(content_dir, "index.md")
        with open(index_md, 'w') as f:
            f.write("# Home Page\n\nWelcome to my site!")
        
        # Create blog subdirectory with a post
        blog_dir = os.path.join(content_dir, "blog")
        os.makedirs(blog_dir)
        post_md = os.path.join(blog_dir, "post1.md")
        with open(post_md, 'w') as f:
            f.write("# My First Post\n\nThis is my first blog post.")
        
        # Create destination
        dest_dir = os.path.join(self.test_dir, "public")
        
        generate_pages_recursive(content_dir, self.template_path, dest_dir)
        
        # Check that all HTML files were created
        expected_files = [
            os.path.join(dest_dir, "index.html"),
            os.path.join(dest_dir, "blog", "post1.html")
        ]
        
        for file_path in expected_files:
            self.assertTrue(os.path.exists(file_path), f"File {file_path} should exist")
    
    def test_generate_pages_recursive_preserves_directory_structure(self):
        """Test that directory structure is preserved."""
        content_dir = os.path.join(self.test_dir, "content")
        os.makedirs(content_dir)
        
        # Create nested structure
        deep_dir = os.path.join(content_dir, "blog", "category")
        os.makedirs(deep_dir)
        deep_post = os.path.join(deep_dir, "deep.md")
        with open(deep_post, 'w') as f:
            f.write("# Deep Post\n\nThis is a deeply nested post.")
        
        dest_dir = os.path.join(self.test_dir, "public")
        generate_pages_recursive(content_dir, self.template_path, dest_dir)
        
        # Check that directories were created
        self.assertTrue(os.path.exists(os.path.join(dest_dir, "blog")))
        self.assertTrue(os.path.exists(os.path.join(dest_dir, "blog", "category")))
        self.assertTrue(os.path.exists(os.path.join(dest_dir, "blog", "category", "deep.html")))
    
    def test_generate_pages_recursive_ignores_non_markdown_files(self):
        """Test that non-markdown files are ignored."""
        content_dir = os.path.join(self.test_dir, "content")
        os.makedirs(content_dir)
        
        # Create a non-markdown file
        txt_file = os.path.join(content_dir, "readme.txt")
        with open(txt_file, 'w') as f:
            f.write("This is not markdown")
        
        dest_dir = os.path.join(self.test_dir, "public")
        generate_pages_recursive(content_dir, self.template_path, dest_dir)
        
        # Check that no HTML file was created for the txt file
        html_file = os.path.join(dest_dir, "readme.html")
        self.assertFalse(os.path.exists(html_file))


if __name__ == "__main__":
    unittest.main()
