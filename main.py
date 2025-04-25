import openai
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful assistant who writes content."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message["content"]

if __name__ == "__main__":
    prompt = "Write a tweet about productivity tips"
    result = generate_response(prompt)
    print(result)
