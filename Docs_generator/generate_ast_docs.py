# galaxy_ast_docs/generate_ast_docs.py
import os
import argparse
from .walker import walk_and_parse
from .output_layer import save_to_json
from .language_layer import available_languages

def main():
    parser = argparse.ArgumentParser(description='Generate hierarchical AST documentation')
    parser.add_argument('--root', default='.', help='Root directory to scan')
    parser.add_argument('--output', default='ast_documentation.json', help='Output file path')
    parser.add_argument('--debug', action='store_true', help='Enable verbose debug output')
    args = parser.parse_args()

    print(f"🔍 Scanning: {os.path.abspath(args.root)}")
    print(f"🌐 Languages supported: {', '.join(available_languages())}")

    results = walk_and_parse(args.root, debug=args.debug)
    save_to_json(results, args.output)

if __name__ == "__main__":
    main()