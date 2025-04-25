import os
from openai import OpenAI
from dotenv import load_dotenv
from openai import RateLimitError

# Load .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who writes content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except RateLimitError as e:
        return "⚠️ Error: You've exceeded your usage quota. Please check your OpenAI billing."


if __name__ == "__main__":
    prompt = "Write a tweet about productivity tips"
    result = generate_response(prompt)
    print(result)
