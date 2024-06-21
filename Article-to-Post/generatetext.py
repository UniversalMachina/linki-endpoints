import os
from dotenv import load_dotenv
from openai import OpenAI
import fitz  # PyMuPDF (this is not used in the chatbot but included per the provided script)

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with API Key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# Function to generate text using OpenAI's Chat Completion
def generate_text(message, model="gpt-4-turbo"):
    messages = [
        {"role": "user", "content": message}]
    try:
        # Create a chat completion
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
        )

        # Access the message content
        message_content = chat_completion.choices[0].message.content
        print(message_content)
        return message_content
    except Exception as e:
        print(f"Error during API call: {e}")
        return "Sorry, I couldn't process your request at the moment."


