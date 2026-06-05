# To run this code you need to install the following dependencies:
# pip install groq python-dotenv

import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from the root .env file
load_dotenv()

def interactive_chat():
    # Initialize the Groq client
    client = Groq()

    system_prompt = """
    You are Seraphina, an Elite Experience Designer at Luxe Horizon Travel with 15+ years of experience curating bespoke, multi-million dollar itineraries for high-net-worth individuals.

    TONE & STYLE:
    Your tone is poised, sophisticated, deeply attentive, and highly articulate. Use elegant vocabulary (e.g., curated, bespoke, seamless, heritage property). Avoid retail buzzwords (e.g., "cheap", "bargain", "deal"). Never use exclamation points (!) or casual slang ("Hey", "No problem").

    STRICT CONSTRAINTS:
    1. COMPETITOR PROTOCOL: Never mention, acknowledge, or validate any third-party booking sites or competitors (e.g., Expedia, Booking.com, Amex Fine Hotels). If a client mentions a competitor or requests a price match, completely ignore the competitor's name. Smoothly pivot the conversation to the exclusive value, private villa contracts, and unlisted VIP perks available only through Luxe Horizon.
    2. DISCOUNT PROTOCOL: Never grant flat percentage discounts (e.g., "10% off" or "saving $1,000"). This cheapens the brand. If a client hesitates on price or demands a discount, address their hesitation by offering an "exclusive, complimentary privilege" or high-end value-add (e.g., private yacht transfers, a curated Michelin-star dining experience, or a complimentary night at a private estate).
    """

    # Initialize the chat history list with the system guidelines
    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    print("====================================================")
    print("  Seraphina is online. Type 'exit' to end the chat. ")
    print("====================================================\n")

    while True:
        # 1. Get live input from you in the terminal
        user_message = input("You: ")
        
        # 2. Check if you want to leave
        if user_message.strip().lower() == 'exit':
            print("\nSeraphina: It has been an absolute privilege assisting you. I wish you a seamless journey ahead. Goodbye.")
            break
            
        # Skip empty inputs
        if not user_message.strip():
            continue

        # 3. Append your new message to the ongoing conversation history
        messages.append({"role": "user", "content": user_message})

        print("\nSeraphina: ", end="")

        # 4. Request streaming completion from Groq using the full history
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.3,
            stream=True,
        )

        # 5. Capture the incoming response text to save it later
        assistant_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                token = chunk.choices[0].delta.content
                print(token, end="")
                assistant_response += token
                
        print("\n") # New line after stream ends

        # 6. Append Seraphina's response to history so she remembers it next turn
        messages.append({"role": "assistant", "content": assistant_response})

if __name__ == "__main__":
    interactive_chat()
