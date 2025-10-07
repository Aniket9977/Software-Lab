from config import *
def frontend_agent(frontend_tasks):
    prompt = f"""
    You are a React developer.
    Based on these frontend requirements:
    {frontend_tasks}
    Generate React component code using functional components, Tailwind CSS, and React Router.
    Give me only the code that is not in comment it should be working fine directly
    """
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"user","content":prompt}]
    )
    return resp.choices[0].message.content
