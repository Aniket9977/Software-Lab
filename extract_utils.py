# extract_utils.py
import json
import re
from typing import Optional

def extract_section(plan_str: str, section_name: str) -> Optional[str]:
    """
    Extracts a named section (e.g., 'Frontend Tasks' or 'Backend Tasks')
    from a JSON or text plan returned by the coordinator agent.
    """
    if not plan_str:
        return None

    # Try parsing as JSON first
    try:
        plan = json.loads(plan_str)
        if isinstance(plan, dict):
            for k, v in plan.items():
                if k.lower() == section_name.lower():
                    return v if isinstance(v, str) else json.dumps(v, indent=2)
    except json.JSONDecodeError:
        pass

    # Try Markdown-style headings
    pattern = rf"(^#+\s*{re.escape(section_name)}\s*$)(.*?)(?=^#|\Z)"
    m = re.search(pattern, plan_str, flags=re.IGNORECASE | re.DOTALL | re.MULTILINE)
    if m:
        return m.group(2).strip()

    # Try key: value or label style
    pattern2 = rf"{re.escape(section_name)}\s*:\s*(.*?)(?=\n\s*\w+\s*:|\Z)"
    m2 = re.search(pattern2, plan_str, flags=re.IGNORECASE | re.DOTALL)
    if m2:
        return m2.group(1).strip()

    # Fallback: line-by-line search
    lines = plan_str.splitlines()
    try:
        idx = next(i for i, line in enumerate(lines) if section_name.lower() in line.lower())
        collected = []
        for ln in lines[idx+1:]:
            if not ln.strip():
                break
            collected.append(ln)
        return "\n".join(collected).strip() or None
    except StopIteration:
        return None
