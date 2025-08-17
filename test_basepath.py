#!/usr/bin/env python3

import os
import sys
import tempfile
import shutil

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from generate_page import generate_page, generate_pages_recursive

def test_basepath_functionality():
    """Test that basepath parameter works correctly"""
    print("Testing basepath functionality...")
    
    # Create temporary directories
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create content directory
        content_dir = os.path.join(temp_dir, "content")
        os.makedirs(content_dir)
        
        # Create template
        template_path = os.path.join(temp_dir, "template.html")
        with open(template_path, 'w') as f:
            f.write('<!DOCTYPE html><html><head><title>{{ Title }}</title><link href="/index.css" rel="stylesheet"></head><body>{{ Content }}</body></html>')
        
        # Create markdown content
        md_path = os.path.join(content_dir, "test.md")
        with open(md_path, 'w') as f:
            f.write('# Test Page\n\nThis is a test with a [link](/home) and ![image](/img.png).')
        
        # Test with default basepath
        dest_dir = os.path.join(temp_dir, "docs")
        generate_page(md_path, template_path, os.path.join(dest_dir, "test.html"), "/")
        
        with open(os.path.join(dest_dir, "test.html"), 'r') as f:
            content_default = f.read()
        
        print("Default basepath (/): ")
        print("  CSS link:", 'href="/index.css"' in content_default)
        print("  Link:", 'href="/home"' in content_default) 
        print("  Image:", 'src="/img.png"' in content_default)
        
        # Test with GitHub Pages basepath
        shutil.rmtree(dest_dir)
        generate_page(md_path, template_path, os.path.join(dest_dir, "test.html"), "/static-site-gen/")
        
        with open(os.path.join(dest_dir, "test.html"), 'r') as f:
            content_ghpages = f.read()
        
        print("\nGitHub Pages basepath (/static-site-gen/): ")
        print("  CSS link:", 'href="/static-site-gen/index.css"' in content_ghpages)
        print("  Link:", 'href="/static-site-gen/home"' in content_ghpages)
        print("  Image:", 'src="/static-site-gen/img.png"' in content_ghpages)
        
        # Verify the replacements worked
        assert 'href="/static-site-gen/index.css"' in content_ghpages
        assert 'href="/static-site-gen/home"' in content_ghpages  
        assert 'src="/static-site-gen/img.png"' in content_ghpages
        
        print("\n✅ All basepath tests passed!")

if __name__ == "__main__":
    test_basepath_functionality()
