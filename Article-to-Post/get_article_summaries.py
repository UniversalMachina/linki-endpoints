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


def get_news_articles(api_key, query, page_size=10):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'apiKey': api_key,
        'pageSize': page_size
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return articles
    else:
        print(f"Failed to fetch articles: {response.status_code}")
        return []


def linkfilter(text):
    # Implement your linkfilter logic here
    # This is a placeholder function
    return text


def get_text(link):
    downloaded = trafilatura.fetch_url(link)
    if downloaded:
        articletext = trafilatura.extract(downloaded)
        if articletext:
            articletext2 = linkfilter(articletext)
            return articletext2
        else:
            print("Could not extract the article text.")
            return None
    else:
        print("Failed to download the article.")
        return None


def generate_summary(article_text):
    # Assume generate_text is a function that summarizes the text
    prompt = f"Summarize the following article:\n\n{article_text}\n\nSummary:"
    summary = generate_text(prompt)
    return summary


def summarize_articles_to_string(api_key, query, page_size=5):
    articles = get_news_articles(api_key, query, page_size)
    output = []

    for i, article in enumerate(articles, 1):
        print(f"Processing article {i}: {article['title']}")
        article_text = get_text(article['url'])
        if article_text:
            summary = generate_summary(article_text)
            output.append(
                f"{i}. {article['title']}\n   Source: {article['source']['name']}\n   URL: {article['url']}\n   Published At: {article['publishedAt']}\n   Summary: {summary}\n")
        else:
            print(f"Skipping article {i} due to extraction failure.")

    return "\n".join(output)


import re


def check_alphanumeric(summarized_articles_string):
    if summarized_articles_string is None:
        return "could not find article"

    # Remove all spaces, empty lines, and line breaks
    clean_string = re.sub(r'\s+', '', summarized_articles_string)

    # Check for alphanumeric characters
    if re.search(r'[a-zA-Z0-9]', clean_string):
        return True
    else:
        return False



def getarticlesummaries(query = 'Artificial Intelligence'):
    api_key = '1e122eff2e0b493da33b20990695a541'  # Replace with your News API key
    summarized_articles_string = summarize_articles_to_string(api_key, query)

    print(summarized_articles_string)
    # result = check_alphanumeric(summarized_articles_string)
    # print(result)
    if check_alphanumeric(summarized_articles_string):
        return "could not find article"
    return summarized_articles_string

if __name__ == "__main__":
    # Example usage
    text=getarticlesummaries("MBSR workshops and activities")
    print(text)