# File: galaxy-docs/ast_parser.py
# Purpose: This script walks through the Galaxy-App Python files,
# parses their AST, extracts function and class information,
# and generates beginner-friendly Markdown documentation.


# File: galaxy-docs/generate_docs.py
import os
from pathlib import Path
from ast_tools.parser_layer import parse_python_file
from ast_tools.traversal_layer import extract_functions, extract_classes
from ast_tools.render_layer import write_markdown

def generate_docs():
    base_dir = Path(__file__).parent.parent  # Goes up to project root
    source_files = {
        'main': base_dir / 'galaxy_app/main.py',
        'schemas': base_dir / 'galaxy_app/models/schemas.py'
    }
    output_dir = Path(__file__).parent / 'docs/auto-docs'

    for name, path in source_files.items():
        tree = parse_python_file(str(path))  # Convert to string for open()
        functions = extract_functions(tree)
        classes = extract_classes(tree)
        write_markdown(name, functions, classes, output_dir)


if __name__ == "__main__":
    generate_docs()
    print(" AST documentation written to galaxy-docs/docs/auto-docs/")

