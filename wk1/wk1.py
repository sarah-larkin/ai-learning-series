import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)


# #simple text generation: 
# model = genai.GenerativeModel('gemini-2.5-flash-lite')
# response = model.generate_content("What is AI?")
# print(response.text)


# #simple text generation with system prompt
# model = genai.GenerativeModel(
#     'gemini-2.5-flash-lite',
#     system_instruction="You are a helpful AI teacher. Explain concepts simply."
# )
# response = model.generate_content("What is AI?")
# print(response.text)


# #Streaming response
# model = genai.GenerativeModel('gemini-2.5-flash-lite')
# response = model.generate_content(
#     "Write a short story about AI",
#     stream=True
# )

# for chunk in response:
#     print(chunk.text, end="")


#With configuration - NOT WORKING
model = genai.GenerativeModel('gemini-2.5-flash-lite')
response = model.generate_content(
    "Write a creative story",
    generation_config=genai.types.GenerationConfig(
        temperature=0.9,  # More creative (0-2)
        top_p=0.95,       # Diversity
        max_output_tokens=1000
    )
)
