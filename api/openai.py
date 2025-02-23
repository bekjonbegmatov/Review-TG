from openai import OpenAI
from config import open_ai_api_key

client = OpenAI(
    api_key=open_ai_api_key,
    base_url="https://api.proxyapi.ru/openai/v1",
)

def ask_ai(messages: list) -> str:
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}. Please try again later."
