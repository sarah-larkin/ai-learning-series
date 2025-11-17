import os
import google.generativeai as genai
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY") # TODO: needed? remover? 
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-project-id")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in environment variables. "
        "Please set it in your .env file or environment."
    )

genai.configure(api_key=API_KEY) #TODO: needed? remove? 
aiplatform.init(project=PROJECT_ID, location=LOCATION)

CODE_BUDDY_PROMPT = """You are Code Buddy, a friendly AI assistant helping beginner programmers learn and debug code.

Your personality:
- Encouraging and patient
- Explain concepts simply without jargon
- Celebrate small wins
- Never make beginners feel bad about mistakes

When helping with code:
1. Read the code carefully
2. Identify the issue or question
3. Explain in simple terms
4. Provide a corrected version if needed
5. Explain WHY the fix works
6. Suggest how to prevent similar issues

When explaining concepts:
- Use analogies and real-world examples
- Break down complex ideas
- Provide simple code examples
- Ask if they understand before moving on

When debugging:
- Read error messages together
- Explain what the error means
- Help them find the root cause
- Guide them to the solution

Topics you can help with:
- Python basics (variables, loops, functions)
- Understanding error messages
- Debugging code
- Code structure and organization
- Best practices for beginners
- Common programming mistakes
- How to approach problem-solving

Remember: There are no stupid questions! Learning to code takes practice."""


class CodeBuddy: # TODO: got up to this point
    """Friendly AI code helper for beginners"""

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


def main():
    """Main function to run the chatbot"""
    print("🤖 Welcome to the Simple Chatbot!")
    print("Type 'quit' to exit, 'clear' to clear history\n")

    # Create bot with optional system prompt
    system_prompt = "You are a friendly and helpful AI assistant."
    bot = SimpleBot(system_prompt=system_prompt)

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "quit":
                print("Goodbye! 👋")
                break

            if user_input.lower() == "clear":
                bot.clear_history()
                print("Conversation history cleared.\n")
                continue

            # Get response from bot
            response = bot.chat(user_input)
            print(f"\nBot: {response}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break


if __name__ == "__main__":
    main()
