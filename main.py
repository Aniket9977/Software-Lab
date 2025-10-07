import json
import os
import re
import pathlib
from coordinator import coordinator_agent
from frontend import frontend_agent
from backend import backend_agent
from extract_utils import extract_section

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

    with open("frontend_output.js", "w", encoding="utf-8") as f:
        f.write(frontend_code)

    with open("backend_output.py", "w", encoding="utf-8") as f:
        f.write(backend_code)

    print("All outputs saved ")



if __name__ == "__main__":
    main()
# i want a wesbite that store the name and email and disply them