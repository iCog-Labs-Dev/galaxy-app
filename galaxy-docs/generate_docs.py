# File: galaxy-docs/generate_docs.py
import os
from pathlib import Path
from ast_tools.parser_layer import parse_python_file
from ast_tools.traversal_layer import extract_functions, extract_classes
from ast_tools.render_layer import write_markdown

def generate_docs():
    base_dir = Path(__file__).parent.parent  # Root: galaxy-app/
    source_dir = base_dir / 'galaxy_app'     # Source Python files directory
    output_dir = Path(__file__).parent / 'docs/auto-docs'

    # Step 1: Recursively gather all `.py` files in galaxy_app/
    py_files = list(source_dir.rglob('*.py'))

    # Step 2: Loop through each file and parse/extract/render
    for file_path in py_files:
        tree = parse_python_file(str(file_path))
        functions = extract_functions(tree)
        classes = extract_classes(tree)

        # Step 3: Generate relative file name (used as Markdown file name)
        relative_path = file_path.relative_to(source_dir)  # e.g., models/schemas.py
        doc_name = str(relative_path.with_suffix('')).replace(os.sep, '_')  # e.g., models_schemas

        write_markdown(doc_name, functions, classes, output_dir)

    print(f"AST documentation generated for {len(py_files)} files in `{output_dir}`")

if __name__ == "__main__":
    generate_docs()
