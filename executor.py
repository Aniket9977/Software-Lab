import os
import re

# Paths
FRONTEND_DIR = "frontend_app/src/components"
BACKEND_DIR = "backend_app"

# Make sure directories exist
os.makedirs(FRONTEND_DIR, exist_ok=True)
os.makedirs(BACKEND_DIR, exist_ok=True)

def execute_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into code blocks ```lang ... ```
    code_blocks = re.findall(r"```(\w+)\n(.*?)```", content, flags=re.DOTALL)

    for lang, code in code_blocks:
        code = code.strip()
        if lang.lower() in ("jsx", "react"):
            # Extract component name from first line
            match = re.search(r"function (\w+)\(", code)
            if match:
                component_name = match.group(1)
            else:
                # fallback
                component_name = "App"

            file_name = f"{component_name}.jsx"
            file_path = os.path.join(FRONTEND_DIR, file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"✅ Wrote React component: {file_path}")

        elif lang.lower() in ("python", "py"):
            # For backend Python code
            # Extract first function name or default
            match = re.search(r"def (\w+)\(", code)
            file_name = f"{match.group(1) if match else 'backend'}.py"
            file_path = os.path.join(BACKEND_DIR, file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"✅ Wrote Python backend: {file_path}")
            # Optionally execute
            # exec(code, globals())

        else:
            print(f"⚠️ Unknown code language: {lang}, skipping.")

