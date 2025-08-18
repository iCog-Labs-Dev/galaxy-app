import os
from tree_sitter import Language, Parser

HERE = os.path.dirname(__file__)
BUILD_DIR = os.path.join(HERE, "build")
LIB_PATH = os.path.join(BUILD_DIR, "my-languages.so")

PARSERS = {
    "python": "tree-sitter-python",
    "javascript": "tree-sitter-javascript",
    "java": "tree-sitter-java",
}

EXT_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".java": "java",
}

_LANGS = {}

def _ensure_built():
    if not os.path.exists(LIB_PATH):
        raise RuntimeError(
            f"Tree-sitter language library not found at: {LIB_PATH}\n"
            "Please build it by running:\n"
            "  python -m galaxy_ast_docs.build_parsers\n"
        )

def _load_languages():
    _ensure_built()
    for name in PARSERS.keys():
        if name in _LANGS:
            continue
        try:
            _LANGS[name] = Language(LIB_PATH, name)
        except Exception as e:
            raise RuntimeError(f"Failed to load language '{name}': {e}")

def get_parser(lang_name):
    if lang_name not in _LANGS:
        _load_languages()
    parser = Parser()
    parser.set_language(_LANGS[lang_name])
    return parser

def detect_language(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return EXT_MAP.get(ext)

def available_languages():
    return list(EXT_MAP.values())

# (Optionally ) but currenty we not used here version for language
def get_language_version(lang_name):
    """Get the version of the loaded language parser"""
    _load_languages()
    if lang_name in _LANGS:
        return _LANGS[lang_name].version
    return None

# Add this to the __init__.py or keep it here