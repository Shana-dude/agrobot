import requests
import os
from .embedding import get_embeddings
from .vector_store import VectorStore
from .ingest import extract_text, chunk_text
from .config import HUGGINGFACE_API_KEY, HF_MODEL, AGMARKNET_API_KEY, OPENWEATHER_API_KEY
from .market_api import get_tomato_prices
from .weather_api import get_weather

# ✅ Updated Hugging Face Router URL (OpenAI-compatible)
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

vector_store = None


# ===============================
# RAG SETUP
# ===============================

def setup_rag():
    global vector_store

    if not HUGGINGFACE_API_KEY or "your_huggingface_api_key_here" in HUGGINGFACE_API_KEY:
        print("WARNING: HUGGINGFACE_API_KEY is not set or is still the placeholder. RAG will build but LLM calls will fail.")

    print("Building vector index from PDF...")

    try:
        text = extract_text()
        if not text:
            print("Error: No text extracted from PDF.")
            return

        chunks = chunk_text(text)
        if not chunks:
            print("Error: PDF text could not be chunked.")
            return

        embeddings = get_embeddings(chunks)
        if len(embeddings) == 0:
            print("Error: No embeddings generated.")
            return

        vector_store = VectorStore(len(embeddings[0]))
        vector_store.add(embeddings, chunks)
        vector_store.save()

        print("Vector index created and saved.")
    except Exception as e:
        print(f"Error during RAG setup: {e}")


def load_rag():
    global vector_store

    print("Loading existing vector index...")
    vector_store = VectorStore(384)
    vector_store.load()
    print("Vector index loaded.")


# ===============================
# HUGGING FACE CALL (MODERN CHAT API)
# ===============================

def call_huggingface_llm(prompt):

    payload = {
        "model": HF_MODEL,
        "messages": [
            {"role": "system", "content": "You are AgroBot, a helpful agricultural expert."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.3
    }

    try:
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        print("HF Status Code:", response.status_code)

        # ❌ If unauthorized
        if response.status_code == 401:
            return "Error 401: Unauthorized. Please check your HUGGINGFACE_API_KEY in the .env file. Ensure it is a valid token from huggingface.co."
        
        # ❌ If not successful response
        if response.status_code != 200:
            return f"HuggingFace Error {response.status_code}: {response.text}"

        # Try parsing JSON safely
        try:
            result = response.json()
            content = result["choices"][0]["message"]["content"].strip()
            # Remove markdown artifacts for cleaner farmer-friendly text
            clean_content = content.replace("**", "").replace("*", "").replace("###", "").replace("##", "")
            return clean_content
        except Exception as e:
            return f"Error parsing HF response: {str(e)} | Response: {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"


# ===============================
# MAIN RAG ANSWER FUNCTION
# ===============================

def answer_question(question, lat=None, lon=None):

    if vector_store is None:
        return "Vector store not initialized."

    # Step 1: Embed user query
    query_embedding = get_embeddings([question])

    # Step 2: Retrieve top chunks
    context_chunks = vector_store.search(query_embedding)
    context = "\n".join(context_chunks)

    # Step 2.5: Inject Real-time Market Data if requested
    market_keywords = ["price", "market", "rate", "mandi", "விலை", "சந்தை"]
    if any(kw in question.lower() for kw in market_keywords):
        market_data = get_tomato_prices()
        context = f"REAL-TIME MARKET DATA:\n{market_data}\n\nUSER PDF KNOWLEDGE:\n{context}"

    # Step 2.6: Inject Real-time Weather Data if requested (GPS-enhanced)
    weather_keywords = ["weather", "rain", "temperature", "climate", "வானிலை", "மழை"]
    if any(kw in question.lower() for kw in weather_keywords):
        weather_data = get_weather(lat=lat, lon=lon)
        context = f"LIVE WEATHER DATA:\n{weather_data}\n\nUSER PDF KNOWLEDGE:\n{context}\n\nINSTRUCTION: Provide farming advice based on this weather (e.g., irrigation if hot, protection if rain)."

    # Step 3: Build grounded prompt
    prompt = f"""
You are AgroBot, a wise agricultural expert. Answer concisely using the guide.

Guide:
{context}

Question: {question}

INSTRUCTIONS:
1. Provide a concise but complete answer in BOTH English and Tamil.
2. IMPORTANT: Use ONLY TAMIL SCRIPT (தக்காளி). Never use Romaji.
3. Keep the total response under 300 words for speed.

FORMAT:
English: [Concise Advice]
Tamil: [எளிமையான தமிழ் விளக்கம்]
"""

    # Step 4: Call LLM
    return call_huggingface_llm(prompt)
