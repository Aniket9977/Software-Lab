from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)




def coordinator_agent(project_brief):
    # Step 1: Break down project brief
    task_prompt = f"""
    You are a senior software architect.
    Given this project brief: "{project_brief}"
    Break it into technical tasks divided into:
    - Frontend Tasks
    - Backend Tasks
    Return in JSON format.
    """
    tasks = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role":"user","content":task_prompt}]
    )
    task_plan = tasks.choices[0].message.content
    return task_plan
