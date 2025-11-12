from dotenv import load_dotenv
import os

load_dotenv()

project_id = os.getenv("GCP_PROJECT_ID")
location = os.getenv("GCP_LOCATION")