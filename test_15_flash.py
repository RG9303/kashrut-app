import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content("Say hello")
    print(f"Success! Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
