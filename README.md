# Caption Edit Tool

A powerful bulk text file editor that allows you to make systematic changes across multiple text files.

## What is Caption Edit?

Caption Edit is a Python-based command-line tool designed to help you perform bulk text editing operations on multiple text files (.txt) at once. It's particularly useful for situations where you need to make consistent changes across a large number of files, such as:

- Updating terminology throughout a documentation set
- Standardizing formatting in caption files
- Adding headers or footers to multiple text documents
- Making global replacements across a collection of text files

## Features

- **Find and Replace**: Replace specific text strings across all files
- **Prepend Text**: Add text to the beginning of each file
- **Append Text**: Add text to the end of each file
- **Recursive Directory Scanning**: Process files in subdirectories
- **Output Options**: Edit files in-place or output to a new location
- **Safety Confirmation**: Review and confirm before making changes
- **Error Logging**: Detailed error tracking with timestamps

## Requirements

- Windows operating system
- Python 3.6 or higher

This tool uses only standard Python libraries, so no additional installation is required.

## Usage

### Running the Tool

To run the Caption Edit tool, use the provided batch file:

```
run.bat [options]
```

Alternatively, you can run the Python script directly:

```
python caption-edit.py [options]
```

### Command-Line Options

| Option | Description | Required |
|--------|-------------|----------|
| `--path PATH` | Directory path to scan for .txt files | Yes |
| `--target STRING` | Target string to search for | Yes |
| `--swap STRING` | Replacement string | Yes |
| `--prepend STRING` | Text to add at the beginning of each file | No |
| `--append STRING` | Text to add at the end of each file | No |
| `--recursive` | Recursively scan subdirectories | No |
| `--output PATH` | Output directory for edited files (default is in-place editing) | No |

### Example Usage

#### Basic Find and Replace

```
run.bat --path "C:\Documents\Captions" --target "Hello" --swap "Hi"
```
This will replace all instances of "Hello" with "Hi" in all .txt files in the specified directory.

#### Adding Text to Files

```
run.bat --path "C:\Documents\Captions" --target "" --swap "" --prepend "DISCLAIMER: " --append "\nEND OF FILE"
```
This will add "DISCLAIMER: " to the beginning and "END OF FILE" on a new line at the end of each .txt file. Note that you still need to provide the `--target` and `--swap` parameters, but they can be empty strings if you only want to prepend or append.

#### Recursive Processing with Output Directory

```
run.bat --path "C:\Documents\Captions" --target "old term" --swap "new term" --recursive --output "C:\Documents\Edited_Captions"
```
This will:
1. Scan the "C:\Documents\Captions" directory and all its subdirectories for .txt files
2. Replace all instances of "old term" with "new term"
3. Save the modified files to "C:\Documents\Edited_Captions", preserving the original directory structure

### Step-by-Step Guide

1. **Prepare Your Files**:
   - Organize the text files you want to edit in a directory
   - Identify the text you want to find and replace

2. **Run the Tool**:
   - Open a command prompt
   - Navigate to the directory containing the Caption Edit tool
   - Run the tool with appropriate options (as shown in examples above)

3. **Review and Confirm**:
   - The tool will display the files it found and ask for confirmation
   - Review the list to ensure it matches your expectations
   - Type 'y' to proceed or 'n' to cancel

4. **Check Results**:
   - After processing, the tool will display a summary
   - If any errors occurred, check the log file for details

## Error Handling

If any errors occur during processing, the tool will:
1. Continue processing other files
2. Count the number of errors
3. Generate a timestamped log file with error details
4. Display the path to the log file

## For Developers

### Project Structure

```
caption-edit/
├── caption-edit.py     # Main Python script
├── run.bat             # Windows batch script to run the tool
└── README.md           # Documentation
```

### Dependencies

The tool currently uses only standard Python library modules:
- `os`, `sys`: System operations
- `argparse`: Command-line argument parsing
- `datetime`: Timestamp generation for logs
- `shutil`: File operations
- `pathlib`: Path handling

### Extending the Tool

The Caption Edit tool is designed to be extensible. Some potential areas for enhancement:
- Support for additional file types
- Regular expression pattern matching
- Preview mode for changes
- Additional text transformation options
- GUI interface

## License

[Insert your preferred license information here]
