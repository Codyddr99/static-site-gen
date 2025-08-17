import unittest
import os
import tempfile
import shutil
from copy_static import copy_files_recursive


class TestCopyStatic(unittest.TestCase):
    
    def setUp(self):
        """Set up temporary directories for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.test_dir, "source")
        self.dest_dir = os.path.join(self.test_dir, "dest")
        
        # Create source directory structure
        os.mkdir(self.source_dir)
        
        # Create some test files
        with open(os.path.join(self.source_dir, "test.txt"), "w") as f:
            f.write("test content")
        
        # Create a subdirectory with a file
        subdir = os.path.join(self.source_dir, "subdir")
        os.mkdir(subdir)
        with open(os.path.join(subdir, "nested.txt"), "w") as f:
            f.write("nested content")
    
    def tearDown(self):
        """Clean up temporary directories."""
        shutil.rmtree(self.test_dir)
    
    def test_copy_files_recursive_creates_destination(self):
        """Test that the function creates the destination directory."""
        copy_files_recursive(self.source_dir, self.dest_dir)
        self.assertTrue(os.path.exists(self.dest_dir))
    
    def test_copy_files_recursive_copies_files(self):
        """Test that files are copied correctly."""
        copy_files_recursive(self.source_dir, self.dest_dir)
        
        # Check that the main file was copied
        dest_file = os.path.join(self.dest_dir, "test.txt")
        self.assertTrue(os.path.exists(dest_file))
        
        with open(dest_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "test content")
    
    def test_copy_files_recursive_copies_subdirectories(self):
        """Test that subdirectories and nested files are copied."""
        copy_files_recursive(self.source_dir, self.dest_dir)
        
        # Check that subdirectory was created
        dest_subdir = os.path.join(self.dest_dir, "subdir")
        self.assertTrue(os.path.exists(dest_subdir))
        
        # Check that nested file was copied
        dest_nested_file = os.path.join(dest_subdir, "nested.txt")
        self.assertTrue(os.path.exists(dest_nested_file))
        
        with open(dest_nested_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "nested content")
    
    def test_copy_files_recursive_cleans_destination(self):
        """Test that existing destination content is removed."""
        # Create destination with some existing content
        os.mkdir(self.dest_dir)
        existing_file = os.path.join(self.dest_dir, "existing.txt")
        with open(existing_file, "w") as f:
            f.write("existing content")
        
        copy_files_recursive(self.source_dir, self.dest_dir)
        
        # Check that existing file was removed
        self.assertFalse(os.path.exists(existing_file))
        
        # Check that new files were copied
        dest_file = os.path.join(self.dest_dir, "test.txt")
        self.assertTrue(os.path.exists(dest_file))


if __name__ == "__main__":
    unittest.main()
