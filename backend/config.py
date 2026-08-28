"""
Configuration module for the Google GenAI Enterprise & ADK Multi-Agent Stack.
"""

import os
import logging

# Ensure environment flags comply with GEMINI.md enterprise guidelines
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "true")
os.environ["GOOGLE_CLOUD_PROJECT"] = os.getenv("GOOGLE_CLOUD_PROJECT", "arsanjani-genai")
os.environ["GOOGLE_CLOUD_LOCATION"] = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]
MODEL_ID = os.getenv("GENAI_MODEL_ID", "gemini-2.5-flash")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(name)s:%(lineno)d] - %(message)s"
)
logger = logging.getLogger("loan_underwriting")

def get_genai_client():
    """
    Initializes and returns the unified Google GenAI client configured for Vertex AI Enterprise.
    """
    try:
        from google import genai
        client = genai.Client(
            enterprise=True,
            project=PROJECT_ID,
            location=LOCATION
        )
        return client
    except Exception as e:
        logger.warning(f"Could not initialize live Vertex AI Client ({e}). Sandbox/mock mode will be available.")
        return None
