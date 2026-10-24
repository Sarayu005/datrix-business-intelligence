import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY was not found in .env")
else:
    try:
        client = genai.Client(
            api_key=api_key,
            http_options={"timeout": 15000}
        )

        print("Sending test request to Gemini...")

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents="Reply with exactly: Gemini connection works"
        )

        print("Gemini response:", response.text)

    except Exception as exc:
        print("Gemini request failed.")
        print(type(exc).__name__, str(exc))