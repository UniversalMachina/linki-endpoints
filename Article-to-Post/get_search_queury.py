import requests
import trafilatura

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

def getsearchqueury(message="Start building AI apps in minutes using the high performance and reliability of Pinecone’s fully managed vector database on AWS."):
    prompt=f"""given this text write a subject i can use for search, 
    
    example 
    
    INPUT
    Start building AI apps in minutes using the high performance and reliability of Pinecone’s fully managed vector database on AWS.
    
    OUTPUT
    
    Pinecone AI APPS
    
    INPUT
    Answer 10 questions to test your deep learning skills.

    OUTPUT
    deep learning skills
    
    
    INPUT
    Over the course of eight weeks, weekly group workshops and daily mindfulness activities to practice at home comprise the therapeutic intervention known as mindfulness-based stress reduction, or MBSR. Through yoga and medit
    
    OUTPUT
    
    Yoga
    
    
    \n{message}"""
    text=generate_text(prompt)
    return text


if __name__ == "__main__":
    # Example usage
    prompt="""
    Looking for a job can be quite a journey 🙇🏼‍♂️

From creating the ideal resume and preparing for nerve-wracking inte
    """
    getsearchqueury(prompt)
