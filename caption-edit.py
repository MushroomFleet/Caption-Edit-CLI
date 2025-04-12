#!/usr/bin/env python3
"""
Caption Edit Tool - Bulk text file editor

This script allows users to perform bulk edits on text files (.txt) including:
- Find and replace text
- Prepend text to the beginning of files
- Append text to the end of files

The script can process files in-place or output to a new location,
and supports recursive directory scanning.
"""

import os
import sys
import argparse
import datetime
import shutil
from pathlib import Path

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Bulk edit .txt files in a directory",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("--path", required=True, help="Directory path to scan for .txt files")
    parser.add_argument("--target", required=True, help="Target string to search for")
    parser.add_argument("--swap", required=True, help="Replacement string")
    parser.add_argument("--prepend", help="Text to add at the beginning of each file")
    parser.add_argument("--append", help="Text to add at the end of each file")
    parser.add_argument("--recursive", action="store_true", help="Recursively scan subdirectories")
    parser.add_argument("--output", help="Output directory for edited files (default is in-place editing)")
    
    return parser.parse_args()

def setup_logging():
    """Set up error logging with a timestamped file."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"caption_edit_log_{timestamp}.txt"
    return log_filename

def scan_directory(directory, recursive=False):
    """
    Scan a directory for .txt files.
    
    Args:
        directory (str): Directory path to scan
        recursive (bool): Whether to scan subdirectories recursively
        
    Returns:
        list: List of paths to .txt files
    """
    txt_files = []
    directory_path = Path(directory)
    
    if not directory_path.exists() or not directory_path.is_dir():
        return txt_files
    
    # Define the pattern to search for .txt files
    pattern = "**/*.txt" if recursive else "*.txt"
    
    # Use pathlib's glob functionality to find all .txt files
    txt_files = [str(file) for file in directory_path.glob(pattern)]
    
    return txt_files

def edit_file_content(content, target, swap, prepend=None, append=None):
    """
    Edit the content of a file according to specified operations.
    
    Args:
        content (str): Original file content
        target (str): String to search for
        swap (str): Replacement string
        prepend (str, optional): Text to add at the beginning
        append (str, optional): Text to add at the end
        
    Returns:
        str: Modified content
    """
    # Replace target with swap
    modified_content = content.replace(target, swap)
    
    # Prepend text if specified
    if prepend:
        modified_content = prepend + modified_content
    
    # Append text if specified
    if append:
        modified_content = modified_content + append
    
    return modified_content

def process_files(files, target, swap, prepend=None, append=None, output_dir=None):
    """
    Process the list of files with the specified edit operations.
    
    Args:
        files (list): List of file paths to process
        target (str): String to search for
        swap (str): Replacement string
        prepend (str, optional): Text to add at the beginning
        append (str, optional): Text to add at the end
        output_dir (str, optional): Output directory for edited files
        
    Returns:
        tuple: (success_count, error_count, error_log)
    """
    success_count = 0
    error_count = 0
    error_log = []
    
    for file_path in files:
        try:
            # Read the original content
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Apply the edits
            modified_content = edit_file_content(content, target, swap, prepend, append)
            
            # Determine where to write the modified content
            if output_dir:
                # Extract the relative path from the source directory
                rel_path = os.path.relpath(file_path, os.path.dirname(files[0]))
                dest_path = os.path.join(output_dir, rel_path)
                
                # Create directory structure if it doesn't exist
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Write to new location
                with open(dest_path, 'w', encoding='utf-8') as file:
                    file.write(modified_content)
            else:
                # Write in-place
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(modified_content)
            
            success_count += 1
            
        except Exception as e:
            error_count += 1
            error_log.append(f"Error processing {file_path}: {str(e)}")
    
    return success_count, error_count, error_log

def confirm_operation(files):
    """
    Ask for user confirmation before processing files.
    
    Args:
        files (list): List of files to be processed
        
    Returns:
        bool: True if user confirms, False otherwise
    """
    print(f"\nFound {len(files)} .txt files to process:")
    
    # Show a sample of files (first 10)
    for i, file_path in enumerate(files[:10]):
        print(f"  - {file_path}")
    
    if len(files) > 10:
        print(f"  ... and {len(files) - 10} more files")
    
    while True:
        response = input("\nProceed with editing these files? (y/n): ").lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please answer with 'y' or 'n'")

def main():
    """Main execution function."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Set up logging
    log_filename = setup_logging()
    
    try:
        # Scan directory for .txt files
        txt_files = scan_directory(args.path, args.recursive)
        
        if not txt_files:
            print(f"No .txt files found in {args.path}" + 
                  (" and its subdirectories" if args.recursive else ""))
            return
        
        # Ask for confirmation
        if not confirm_operation(txt_files):
            print("Operation cancelled by user.")
            return
        
        # Process the files
        success_count, error_count, error_log = process_files(
            txt_files, 
            args.target, 
            args.swap, 
            args.prepend, 
            args.append, 
            args.output
        )
        
        # Print summary
        print(f"\nOperation complete!")
        print(f"Successfully processed: {success_count} files")
        
        if error_count > 0:
            print(f"Errors encountered: {error_count} files")
            print(f"See {log_filename} for details")
            
            # Write errors to log file
            with open(log_filename, 'w', encoding='utf-8') as log_file:
                log_file.write(f"Caption Edit Log - {datetime.datetime.now()}\n")
                log_file.write("="*50 + "\n\n")
                for error in error_log:
                    log_file.write(f"{error}\n")
    
    except Exception as e:
        # Handle any unexpected errors
        print(f"An error occurred: {str(e)}")
        with open(log_filename, 'w', encoding='utf-8') as log_file:
            log_file.write(f"Caption Edit Log - {datetime.datetime.now()}\n")
            log_file.write("="*50 + "\n\n")
            log_file.write(f"Fatal error: {str(e)}\n")
            log_file.write(f"Traceback: {sys.exc_info()}\n")

if __name__ == "__main__":
    main()
