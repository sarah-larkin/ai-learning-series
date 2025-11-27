from google.cloud import aiplatform

# Initialize Vertex AI
aiplatform.init(project="wcc-ai-project", location="us-central1")

# Import the generative model
from vertexai.generative_models import GenerativeModel

# Initialize the model
model = GenerativeModel("gemini-2.5-flash-lite")

# Make a simple request
response = model.generate_content("What is AI?")

print("Response:")
print(response.text)

#TODO:  NOT WORKING!!!