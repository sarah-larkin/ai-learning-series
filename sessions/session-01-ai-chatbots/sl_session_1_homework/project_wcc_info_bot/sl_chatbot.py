import os
import google.generativeai as genai
from dotenv import load_dotenv
import json


# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in environment variables. "
        "Please set it in your .env file or environment."
    )

genai.configure(api_key=API_KEY)


class SimpleBot:
    """A simple chatbot using Gemini API"""

    def __init__(self, system_prompt: str = None):
        """
        Initialize the chatbot.

        Args:
            system_prompt: Optional system prompt to set bot personality
        """
        self.model = genai.GenerativeModel(
            "gemini-2.5-flash-lite",
            system_instruction=system_prompt
        )
        self.system_prompt = system_prompt
        self.conversation_history = []

    def chat(self, user_message: str) -> str:
        """
        Send a message and get a response.

        Args:
            user_message: The user's input message

        Returns:
            The bot's response
        """
        try:
            # Add user message to history
            self.conversation_history.append(
                {"role": "user", "parts": [user_message]}
            )

            # Generate response using conversation history
            response = self.model.generate_content(
                self.conversation_history
            )

            # Extract response text
            bot_response = response.text

            # Add bot response to history
            self.conversation_history.append(
                {"role": "model", "parts": [bot_response]}
            )

            return bot_response

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            return error_msg

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


# def main():
#     """Main function to run the chatbot"""
#     print("🤖 Welcome to the Simple Chatbot!")
#     print("Type 'quit' to exit, 'clear' to clear history\n")

#     # Load WCC FAQs
#     with open("wcc_faqs.json") as f:
#         wcc_data = json.load(f)

#     # Create FAQ context
#     faq_text = "\n".join([
#         f"Q: {faq['question']}\nA: {faq['answer']}"
#         for faq in wcc_data["faqs"]
#     ])

#     # Create system prompt with WCC knowledge
#     system_prompt = f"""You are a friendly WCC (Women Coding Community) assistant.
#     Your role is to help members learn about WCC, answer questions, and encourage participation.

#     Here are the FAQs you should reference:
#     {faq_text}

#     Be warm, encouraging, and inclusive. If you don't know something, suggest they contact the WCC team.
#     """
#     bot = SimpleBot(system_prompt=system_prompt)

#     while True:
#         try:
#             user_input = input("You: ").strip()

#             if not user_input:
#                 continue

#             if user_input.lower() == "quit":
#                 print("Goodbye! 👋")
#                 break

#             if user_input.lower() == "clear":
#                 bot.clear_history()
#                 print("Conversation history cleared.\n")
#                 continue

#             # Get response from bot
#             response = bot.chat(user_input)
#             print(f"\nBot: {response}\n")

#         except KeyboardInterrupt:
#             print("\n\nGoodbye! 👋")
#             break


# if __name__ == "__main__":
#     main()
