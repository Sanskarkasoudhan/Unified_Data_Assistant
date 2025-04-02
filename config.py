import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("❌ GOOGLE_API_KEY environment variable not set.")

# ChromaDB Settings
CHROMA_DB_PATH = "./chroma_db"

# SQLite Settings
SQLITE_DB_PATH = "./data_store.db"

# Chunking Settings
DEFAULT_CHUNK_SIZE = 1000

# Temporary file for visualizations
TEMP_VIZ_FILE = "temp_visualization.py"