# File: galaxy-docs/ast_tools/parser_layer.py
import ast

def parse_python_file(filepath: str) -> ast.AST:
    """Parse a Python file and return its AST."""
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    return ast.parse(source, filename=filepath)
