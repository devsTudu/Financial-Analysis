import os

from agno.models.openai import OpenAIChat
from agno.models.google import Gemini

from dotenv import load_dotenv

load_dotenv()

if os.getenv("OPENAI_API_KEY"):
    model = OpenAIChat()
    print("Using Gemini")
    
elif os.getenv("GOOGLE_API_KEY"):
    model = Gemini(api_key=os.getenv("GOOGLE_API_KEY"))
    print("Using Gemini")
else:
    print("No Gemini API Key Found")