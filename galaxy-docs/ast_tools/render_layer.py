# File: galaxy-docs/ast_tools/render_layer.py
from typing import List, Dict
from pathlib import Path

def write_markdown(file_name: str, functions: List[Dict], classes: List[Dict], output_dir: Path):
    lines = [f"# Documentation for `{file_name}`\n"]

    if classes:
        lines.append("## Classes\n")
        for cls in classes:
            lines.append(f"### Class `{cls['name']}` (line {cls['lineno']})")
            lines.append(f"- Base classes: {', '.join(cls['bases'])}")
            lines.append(f"> {cls['docstring']}\n" if cls['docstring'] else "_No docstring provided._\n")

    if functions:
        lines.append("## Functions\n")
        for fn in functions:
            lines.append(f"### Function `{fn['name']}` (line {fn['lineno']})")
            lines.append(f"- Arguments: {', '.join(fn['args']) or 'None'}")
            lines.append(f"- Calls: {', '.join(fn['calls']) or 'None'}")
            lines.append(f"> {fn['docstring']}\n" if fn['docstring'] else "_No docstring provided._\n")

    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"{file_name}.md"
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
