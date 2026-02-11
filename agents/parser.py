# agents/parser.py
from openai import OpenAI

# Use GitHub's model endpoint
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key="YOUR_GITHUB_TOKEN"  # Use your GitHub Personal Access Token
)

def parse_test(user_input: str):
    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-4o-mini"
        messages=[
            {"role": "system", "content": "You are a UI test parser..."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content