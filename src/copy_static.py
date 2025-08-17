import os
import shutil


def copy_files_recursive(source_dir_path, dest_dir_path):
    """
    Recursively copy all files and directories from source to destination.
    
    This function will:
    1. Delete all contents of the destination directory (clean slate)
    2. Copy all files and subdirectories from source to destination
    3. Log each file copy operation for debugging
    
    Args:
        source_dir_path: Path to the source directory
        dest_dir_path: Path to the destination directory
    """
    print(f"Copying files from {source_dir_path} to {dest_dir_path}")
    
    # Step 1: Clean the destination directory
    if os.path.exists(dest_dir_path):
        print(f"Removing existing destination directory: {dest_dir_path}")
        shutil.rmtree(dest_dir_path)
    
    # Step 2: Create the destination directory
    print(f"Creating destination directory: {dest_dir_path}")
    os.mkdir(dest_dir_path)
    
    # Step 3: Copy all contents recursively
    _copy_directory_contents(source_dir_path, dest_dir_path)
    
    print(f"Finished copying files from {source_dir_path} to {dest_dir_path}")


def _copy_directory_contents(source_dir, dest_dir):
    """
    Helper function to recursively copy directory contents.
    
    Args:
        source_dir: Source directory path
        dest_dir: Destination directory path
    """
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Warning: Source directory {source_dir} does not exist")
        return
    
    # Get all items in the source directory
    items = os.listdir(source_dir)
    
    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_path):
            # Copy file
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            # Create directory and recursively copy its contents
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            print(f"Recursively copying directory: {source_path} -> {dest_path}")
            _copy_directory_contents(source_path, dest_path)


if __name__ == "__main__":
    # Test the function
    import os
    
    # Get the project root directory (parent of src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    source_static = os.path.join(current_dir, "static")
    dest_public = os.path.join(project_root, "public")
    
    print("Testing copy_files_recursive function:")
    copy_files_recursive(source_static, dest_public)
