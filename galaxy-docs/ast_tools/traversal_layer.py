# File: galaxy-docs/ast_tools/traversal_layer.py
import ast
from typing import List, Dict

def extract_functions(tree: ast.AST) -> List[Dict]:
    result = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            doc = ast.get_docstring(node) or None
            call_names = []

            for n in ast.walk(node):
                if isinstance(n, ast.Call):
                    if isinstance(n.func, ast.Name):
                        call_names.append(n.func.id)
                    elif isinstance(n.func, ast.Attribute):
                        chain = []
                        curr = n.func
                        while isinstance(curr, ast.Attribute):
                            chain.insert(0, curr.attr)
                            curr = curr.value
                        if isinstance(curr, ast.Name):
                            chain.insert(0, curr.id)
                        call_names.append(".".join(chain))
                    else:
                        call_names.append("unknown")

            result.append({
                'name': node.name,
                'args': args,
                'docstring': doc,
                'calls': call_names,
                'lineno': node.lineno
            })
    return result

def extract_classes(tree: ast.AST) -> List[Dict]:
    classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            bases = [
                base.id if isinstance(base, ast.Name) else "complex_base"
                for base in node.bases
            ]
            classes.append({
                'name': node.name,
                'bases': bases,
                'docstring': ast.get_docstring(node),
                'lineno': node.lineno
            })
    return classes
