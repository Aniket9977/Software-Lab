import json
import os
import re
from coordinator import coordinator_agent
from frontend import frontend_agent
from backend import backend_agent
from extract_utils import extract_section

def create_backend_files(backend_code: str, base_dir: str = "backend"):
    """
    Parses the backend code markdown and creates the file structure.
    """
    print("\nStep 5: Creating backend files...")
    os.makedirs(base_dir, exist_ok=True)

    # Regex to find file paths in markdown and their corresponding code blocks
    # Looks for patterns like: `app/main.py`**: ```python ... ```
    pattern = re.compile(r"`([\w\./\-_]+)`\*\*:\s*```(\w+)\n(.*?)\n```", re.DOTALL)
    matches = pattern.findall(backend_code)

    for file_path, lang, code in matches:
        full_path = os.path.join(base_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(code.strip())
        print(f"✅ Created backend file: {full_path}")

def main():
    print("AI Agent System — Project Brief to Technical Tasks\n")
    project_brief = input("Enter your project brief:\n> ").strip()

    if not project_brief:
        print("Please provide a non-empty project brief.")
        return

    print("Step 1: Coordinator analyzing project brief...")
    plan = coordinator_agent(project_brief)
    print("\n--- Coordinator Output ---")
    print(plan)

    # Try extracting tasks
    print("Step 2: Extracting frontend & backend tasks...")
    frontend_tasks = extract_section(plan, "Frontend Tasks") or extract_section(plan, "frontend_tasks")
    backend_tasks = extract_section(plan, "Backend Tasks") or extract_section(plan, "backend_tasks")

    if not frontend_tasks and not backend_tasks:
        print("Could not extract tasks from plan. Ensure Coordinator returns structured output.")
        return

    print(" Step 3: Frontend Agent generating code...")
    frontend_code = frontend_agent(frontend_tasks)
    print("Frontend Agent Output:\n")
    print(frontend_code)

    print("Step 4: Backend Agent generating code...")
    backend_code = backend_agent(backend_tasks)
    print(" Backend Agent Output:\n")
    print(backend_code)

    # Combine results for saving
    project_output = {
        "project_brief": project_brief,
        "plan": plan,
        "frontend_tasks": frontend_tasks,
        "backend_tasks": backend_tasks,
        "frontend_code": frontend_code,
        "backend_code": backend_code
    }

    # Save outputs
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(project_output, f, indent=2, ensure_ascii=False)

    # The user did not request changes to frontend file handling, so we keep it.
    # In a future step, this could also be parsed like the backend.
    with open("frontend_output.js", "w", encoding="utf-8") as f: f.write(frontend_code)
    create_backend_files(backend_code, "backend_generated")


    print("All outputs saved ")



if __name__ == "__main__":
    main()
# i want a wesbite that store the name and email and disply them