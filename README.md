# Directory Tree Implementation

## Description
This is a simple implentation of the hierachal nature of directories. Here are the following commands:

`CREATE <path>` - Adds directory <span style='color:orange'>path</span> to the tree. \
`LIST` - Prints an organized structure of the created directories. \
`MOVE <src> <dst>` - Move directory <span style='color:orange'>src</span> to directory <span style='color:orange'>dst</span> in the tree. \
`DELETE <path>` - Remove directory <span style='color:orange'>path</span> from the tree. 

## Instructions
### Running with User Input
To run this application within the shell, run this command in the current working directory:

`python.exe directories.py`

Enter "QUIT" to exit the program.


### Running with Input File
To run this application with an input file, run this command in the current working directory:

`python.exe directories.py <input_file>`

This method can be used to accurately compare the expected output to the actual output of the program. To save the program's console output to a file, you can run this command:

`python.exe directories.py <input_file> > <output_file>`

### Running Unit Tests

To run the unit tests, run this command:

`python.exe -m pytest -v ./tests/test_directories.py`

## Reflections

With additional time, these are the deliverables to be worked on next:
- Increased documentation for functions and code blocks.
- Unit tests to cover more complex inputs.
- Better error handling and custom exceptions.
- Refactoring code to other files for organization.
- Inquired on how input should handled without an input file.
- Brainstorm scaling up program to persist tree on subsequent runs.
