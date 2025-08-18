# galaxy_ast_docs/traversal_layer.py
def extract_definitions(tree, code_bytes, lang_name):
    """
    Extracts structured data:
    - Classes
    - Functions inside classes or standalone
    - Variables inside each function
    - Line count per function
    """
    root_node = tree.root_node
    classes = []
    functions_outside = []

    def node_text(node):
        return code_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="ignore")

    def collect_variables(func_node):
        """Collect variable names inside a function node."""
        vars_found = []

        def walk_var(n):
            if lang_name == "python" and n.type == "assignment":
                if n.child_count >= 1:
                    vars_found.append(node_text(n.children[0]))
            elif lang_name in ["javascript", "typescript"] and n.type == "variable_declarator":
                name_node = n.child_by_field_name("name")
                if name_node:
                    vars_found.append(node_text(name_node))
            elif lang_name == "java" and n.type == "variable_declarator":
                name_node = n.child_by_field_name("name")
                if name_node:
                    vars_found.append(node_text(name_node))
            for c in n.children:
                walk_var(c)

        walk_var(func_node)
        return vars_found

    def walk(node, current_class=None):
        # Classes
        if lang_name == "python" and node.type == "class_definition":
            name_node = node.child_by_field_name("name")
            if name_node:
                current_class = {
                    "type": "class",
                    "name": node_text(name_node),
                    "line": node.start_point[0] + 1,
                    "functions": []
                }
                classes.append(current_class)

        elif lang_name in ["javascript", "typescript"] and node.type in ("class_declaration", "class_definition"):
            name_node = node.child_by_field_name("name")
            if name_node:
                current_class = {
                    "type": "class",
                    "name": node_text(name_node),
                    "line": node.start_point[0] + 1,
                    "functions": []
                }
                classes.append(current_class)

        elif lang_name == "java" and node.type == "class_declaration":
            name_node = node.child_by_field_name("name")
            if name_node:
                current_class = {
                    "type": "class",
                    "name": node_text(name_node),
                    "line": node.start_point[0] + 1,
                    "functions": []
                }
                classes.append(current_class)

        # Functions
        if lang_name == "python" and node.type == "function_definition":
            name_node = node.child_by_field_name("name")
            if name_node:
                func_info = {
                    "name": node_text(name_node),
                    "line": node.start_point[0] + 1,
                    "variables": collect_variables(node),
                    "num_lines": node.end_point[0] - node.start_point[0] + 1
                }
                if current_class:
                    current_class["functions"].append(func_info)
                else:
                    functions_outside.append(func_info)

        elif lang_name in ["javascript", "typescript"] and node.type in ("function_declaration", "method_definition"):
            name_node = node.child_by_field_name("name")
            if name_node:
                func_info = {
                    "name": node_text(name_node),
                    "line": node.start_point[0] + 1,
                    "variables": collect_variables(node),
                    "num_lines": node.end_point[0] - node.start_point[0] + 1
                }
                if current_class:
                    current_class["functions"].append(func_info)
                else:
                    functions_outside.append(func_info)

        elif lang_name == "java" and node.type in ("method_declaration", "constructor_declaration"):
            name_node = node.child_by_field_name("name")
            if name_node:
                func_info = {
                    "name": node_text(name_node),
                    "line": node.start_point[0] + 1,
                    "variables": collect_variables(node),
                    "num_lines": node.end_point[0] - node.start_point[0] + 1
                }
                if current_class:
                    current_class["functions"].append(func_info)
                else:
                    functions_outside.append(func_info)

        for child in node.children:
            walk(child, current_class)

    walk(root_node)
    return {"classes": classes, "functions": functions_outside}
