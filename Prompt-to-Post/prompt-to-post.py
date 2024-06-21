import os
from dotenv import load_dotenv
from openai import OpenAI
import fitz  # PyMuPDF (this is not used in the chatbot but included per the provided script)

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with API Key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# Function to generate text using OpenAI's Chat Completion
def generate_text(message, model="gpt-4o-2024-05-13"):
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




def basicpost(subject="why i hate cows"):

    prompt=f"""    Please write a LinkedIn post based on this example. it should be able to handle any subject, make the exact format is the same, but restructure it based on the subject

    the subject and hook is ***{subject}***

    Here is the example:

    How YOU Can Boost Your Market Share with AI

    Here’s how to do it without feeling overwhelmed:

    You need a rock-solid plan in place.

    A good plan hinges on 3 key factors:

    1/ Data Analysis

    ⤷ The foundation of any successful AI strategy.
    ⤷ Understand your market inside out.
    ⤷ Identify patterns and trends to make informed decisions.

    2/ Personalized Marketing

    ⤷ This is where AI shines.
    ⤷ Tailor your messages to individual customers.
    ⤷ Deliver the right content at the right time to the right people.

    3/ Continuous Improvement

    ⤷ Never stop optimizing.
    ⤷ Use AI to test, learn, and adapt quickly.
    ⤷ Stay ahead of the competition by being agile and responsive.

    How did we put this into action?

    By implementing this strategy, we helped a client boost their market share by 8%! 📈

    Here’s what we did:

    1/ Analyzed customer data to find untapped opportunities.
    2/ Leveraged AI-driven marketing to deliver personalized content.
    3/ Continuously monitored and tweaked our approach based on real-time feedback.

    Two options for you:

    1/ Spend the next few years figuring it out on your own.
    2/ Start now and grab an extra piece of the pie

     ⤷ Let's chat and see how we can achieve similar results for you"""

    return generate_text(prompt)


