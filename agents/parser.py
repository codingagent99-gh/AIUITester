import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize GitHub Models client
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN")
)

def parse_test(user_input: str):
    """Use GitHub Models to parse test instructions"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a UI test parser. Convert user requests into a Python list of test steps.
Return ONLY a Python list in this exact format (no markdown, no explanations):
[{"action": "navigate", "target": "url"}, {"action": "extract", "target": "data"}]

Available actions: navigate, click, type, extract, wait
"""
                },
                {
                    "role": "user",
                    "content": f"Parse this UI test: {user_input}\n\nReturn only the Python list."
                }
            ],
            temperature=0.1,
            max_tokens=500
        )
        
        content = response.choices[0].message.content
        print(f"🤖 GitHub Model Response: {content}")
        return content
        
    except Exception as e:
        print(f"❌ Error calling GitHub Models API: {e}")
        # Fallback to simple parsing
        return simple_parse(user_input)

def simple_parse(user_input: str):
    """Fallback parser if API fails"""
    steps = []
    lower_input = user_input.lower()
    
    # Extract URL
    words = user_input.split()
    url = None
    for word in words:
        if '.com' in word or '.org' in word or '.net' in word:
            url = word if word.startswith('http') else f"https://{word}"
            break
    
    # Parse actions
    if url:
        steps.append({"action": "navigate", "target": url})
    
    if 'list' in lower_input or 'get' in lower_input or 'extract' in lower_input:
        if 'solution' in lower_input:
            steps.append({"action": "extract", "target": "solutions"})
        else:
            steps.append({"action": "extract", "target": "data"})
    
    print(f"📝 Fallback parsed steps: {steps}")
    return str(steps)