from vertexai.generative_models import GenerativeModel
from google.cloud import aiplatform
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-project-id")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")

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

    def __init__(self):
        self.model = GenerativeModel("gemini-2.5-flash-lite")
        self.system_prompt = CODE_BUDDY_PROMPT
        self.conversation_history = []
        self.learning_topics = []
        
    def chat(self, user_message: str) -> str:
        """ Help with code questions"""
        try:
            # Add user message to history
            self.conversation_history.append(
                {"role": "user", "content": user_message}
            )

            # Build messages with system prompt
            messages = [
                {"role": "user", "content": self.system_prompt},
            ]

            # Add conversation history
            for msg in self.conversation_history:
                messages.append(msg)

            # Generate response
            response = self.model.generate_content(
                [msg["content"] for msg in messages]
            )

            bot_response = response.text

            # Add to history
            self.conversation_history.append(
                {"role": "assistant", "content": bot_response}
            )

            return bot_response

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            return error_msg
    
    def explain_error(self, error_message: str) -> str:
        """Explain what an error means"""
        prompt = f"I got this error: {error_message}. Can you explain what it means?"
        return self.chat(prompt)

    def debug_code(self, code_snippet: str) -> str:
        """Help debug a code snippet"""
        prompt = f"Can you help me debug this code?\n\n{code_snippet}"
        return self.chat(prompt)

    def explain_concept(self, concept: str) -> str:
        """Explain a programming concept"""
        prompt = f"Can you explain {concept} in simple terms?"
        return self.chat(prompt)
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


def main():
    """Run Code Buddy chatbot"""
    print("👨‍💻 Welcome to Code Buddy!")
    print("Your friendly AI code helper")
    print("Type 'quit' to exit, 'clear' to clear history\n")

    buddy = CodeBuddy()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            print("Buddy: Great learning with you! Keep coding! 🚀")
            break

        if user_input.lower() == "clear":
            buddy.clear_history()
            print("Buddy: Conversation cleared. Let's start fresh!\n")
            continue

        if not user_input:
            continue

        response = buddy.chat(user_input)
        print(f"\nBuddy: {response}\n")


if __name__ == "__main__":
    main()
