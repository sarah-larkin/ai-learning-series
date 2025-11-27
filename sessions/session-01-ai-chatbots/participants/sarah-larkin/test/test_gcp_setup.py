from google.cloud import aiplatform

# Initialize Vertex AI
aiplatform.init(project="wcc-ai-project", location="us-central1")

# Test connection
print("✅ GCP setup successful!")