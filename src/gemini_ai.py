import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)


def ask_gemini(question, data_summary):

    prompt = f"""
You are an expert Business Data Analyst.

Analyze the following sales data summary:

{data_summary}

Answer the user's question using only the available business data.

User Question:
{question}

Give a clear, professional answer.
If the data is not sufficient to answer the question, say so clearly.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Gemini API Error: {str(e)}"