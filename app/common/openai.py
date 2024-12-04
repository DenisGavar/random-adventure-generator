import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = OpenAI(
    api_key = OPENAI_API_KEY,
)