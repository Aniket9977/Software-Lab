
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

MODEL ="gpt-4o"