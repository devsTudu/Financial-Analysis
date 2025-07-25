import os

from agno.models.openai import OpenAIChat
from agno.models.google import Gemini



if os.getenv("OPENAI_API_KEY"):
    model = OpenAIChat()

elif os.getenv("GOOGLE_API_KEY"):
    model = Gemini()
