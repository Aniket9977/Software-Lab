from config import *
def backend_agent(backend_tasks):
    prompt = f"""
    You are a backend developer.
    Based on these backend requirements:
    {backend_tasks}
    Generate a Python FastAPI backend with routes, models (SQLAlchemy), and sample database schema.
    
    """
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"user","content":prompt}],
        temperature=0.0,
    )
    return resp.choices[0].message.content
