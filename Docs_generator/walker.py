# galaxy_ast_docs/walker.py
import os
import logging
from .language_layer import detect_language, get_parser
from .parser_layer import parse_code
from .traversal_layer import extract_definitions

def build_tree(root_path, debug=False):
    """Recursively builds folder/file tree with AST info for code files."""
    def process_path(path):
        if os.path.isdir(path):
            return {
                "name": os.path.basename(path),
                "path": os.path.abspath(path),
                "type": "folder",
                "children": [process_path(os.path.join(path, child))
                             for child in sorted(os.listdir(path))
                             if not child.startswith('.')]
            }
        else:
            file_info = {
                "name": os.path.basename(path),
                "path": os.path.abspath(path),
                "type": "file"
            }
            lang = detect_language(path)
            if lang:
                try:
                    with open(path, "rb") as f:
                        code_bytes = f.read()
                    parser = get_parser(lang)
                    tree = parse_code(parser, code_bytes)
                    definitions = extract_definitions(tree, code_bytes, lang)
                    file_info.update({
                        "language": lang,
                        "definitions": definitions
                    })
                except Exception as e:
                    if debug:
                        logging.error(f"Error parsing {path}: {e}")
            return file_info

    return process_path(root_path)

def walk_and_parse(root_path, debug=False):
    return build_tree(root_path, debug)
