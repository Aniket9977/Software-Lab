# integration.py
from backend import backend_agent
from frontend import frontend_agent
from coordinator import coordinator_agent
from extract_utils import extract_section  # if you placed the extract helper separately

def ai_system(project_brief: str):
    """
    Full AI pipeline that:
    1. Uses coordinator to break down a project brief.
    2. Extracts frontend & backend tasks.
    3. Passes them to their respective agents.
    4. Returns generated code.
    """
    print("\n🧠 Running Coordinator Agent...")
    plan = coordinator_agent(project_brief)
    print("\n--- Coordinator Output ---\n")
    print(plan)

    print("\n🔍 Extracting Frontend & Backend Tasks...")
    frontend_tasks = extract_section(plan, "Frontend Tasks") or extract_section(plan, "frontend_tasks")
    backend_tasks = extract_section(plan, "Backend Tasks") or extract_section(plan, "backend_tasks")

    if not frontend_tasks and not backend_tasks:
        raise ValueError("❌ Could not extract 'Frontend Tasks' or 'Backend Tasks' from coordinator output.")

    print("\n🧩 Generating Frontend Code...")
    frontend_code = frontend_agent(frontend_tasks)
    print("\n✅ Frontend Code Generated.\n")

    print("\n⚙️ Generating Backend Code...")
    backend_code = backend_agent(backend_tasks)
    print("\n✅ Backend Code Generated.\n")

    # Final combined output
    result = {
        "plan": plan,
        "frontend_tasks": frontend_tasks,
        "backend_tasks": backend_tasks,
        "Frontend": frontend_code,
        "Backend": backend_code
    }

    print("\n✅ Integration complete.")
    return result
