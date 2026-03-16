import os
import ast

backend_dir = r"C:\Users\lulay\Desktop\aplikasi_berbasis_platform-retogen\backend"
output_path = os.path.join(backend_dir, "structure.txt")

with open(output_path, "w", encoding="utf-8") as out:
    for root, dirs, files in os.walk(backend_dir):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for file in files:
            if not file.endswith(".py"):
                continue
            filepath = os.path.join(root, file)
            rel = os.path.relpath(filepath, backend_dir)
            out.write(f"\n[{rel}]\n")
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        out.write(f"  class {node.name} (line {node.lineno})\n")
                    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
                        out.write(f"  {prefix} {node.name} (line {node.lineno})\n")
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            out.write(f"  import {alias.name}\n")
                    elif isinstance(node, ast.ImportFrom):
                        out.write(f"  from {node.module} import {', '.join(a.name for a in node.names)}\n")
            except Exception as e:
                out.write(f"  [parse error: {e}]\n")

print(f"Written to: {output_path}")