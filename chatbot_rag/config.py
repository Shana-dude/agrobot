import os
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HF_MODEL = os.getenv("HF_GEMINI_MODEL")
AGMARKNET_API_KEY = os.getenv("AGMARKNET_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

PDF_PATH = "chatbot_rag/data/tomato.pdf"
INDEX_PATH = "chatbot_rag/index_storage/faiss_index.bin"
CHUNKS_PATH = "chatbot_rag/index_storage/chunks.pkl"
