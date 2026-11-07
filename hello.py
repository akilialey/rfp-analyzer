from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("ANTHROPIC_API_KEY")

if key:
    print("API key loaded successfully.")
else:
    print("Failed to load API key.")
