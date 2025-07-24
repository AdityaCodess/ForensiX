# gemini_ai.py

import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def analyze_files_with_ai(file_list):
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    You are ForensiX, a digital forensics assistant.
    Analyze the following files and provide:
    - Any sensitive or suspicious files
    - Corrupt or unusually named ones
    - File types of interest
    - Brief insights per file if possible

    FILE LIST:
    {file_list}
    """

    response = model.generate_content(prompt)
    return response.text.strip()
