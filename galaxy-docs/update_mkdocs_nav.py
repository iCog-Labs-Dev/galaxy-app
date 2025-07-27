# File: galaxy-docs/update_mkdocs_nav.py
from pathlib import Path

BASE_CONFIG = Path("mkdocs.base.yml")
FINAL_CONFIG = Path("mkdocs.yml")
AUTO_DOCS_DIR = Path("docs/auto-docs")

def generate_nav_entries():
    entries = []
    for md_file in sorted(AUTO_DOCS_DIR.glob("*.md")):
        title = md_file.stem.replace('_', '/') + ".py"  # e.g., models_schemas -> models/schemas.py
        path = f"{AUTO_DOCS_DIR.name}/{md_file.name}"   # e.g., auto-docs/models_schemas.md
        entries.append(f"      - {title}: {path}")       # 6 spaces for correct nesting
    return entries

def update_mkdocs_yml():
    if not BASE_CONFIG.exists():
        print("❌ mkdocs.base.yml not found!")
        return

    with open(BASE_CONFIG, 'r') as f:
        base_lines = f.readlines()

    nav_block = generate_nav_entries()

    output_lines = []
    replaced = False

    for line in base_lines:
        if '__PLACEHOLDER__' in line:
            output_lines.extend(nav_block)
            replaced = True
        else:
            output_lines.append(line.rstrip())

    if not replaced:
        print("⚠️  No placeholder found in base config. Nothing replaced.")
    else:
        with open(FINAL_CONFIG, 'w') as f:
            f.write("\n".join(output_lines) + "\n")
        print(f"✅ Updated `{FINAL_CONFIG}` with AST Explorer navigation.")

if __name__ == "__main__":
    update_mkdocs_yml()
