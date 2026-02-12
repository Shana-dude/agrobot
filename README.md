# AgroBot: Tomato Farming Expert Chatbot

AgroBot is a specialized, bilingual AI assistant designed for tomato farmers. It combines expert knowledge from agricultural guides with real-time field data (Weather & Market Prices) to provide actionable, location-specific advice.

## 🚀 Key Features

- **Expert Knowledge (RAG)**: Uses Retrieval-Augmented Generation to answer questions based on a professional Tomato Farming PDF guide.
- **Bilingual Support**: Full text and audio support in both **English and Tamil**.
- **Real-Time Market Prices**: Integrated with **Agmarknet (data.gov.in)** to provide current wholesale prices (Mandi rates).
- **GPS-Based Weather**: Automatically detects user location to provide live weather and tailored farming suggestions via **OpenWeather API**.
- **Farmer-Friendly UI**: Simple, high-contrast professional design optimized for outdoor use.
- **Voice Capabilities**: 
  - **Speech-to-Text**: Farmers can speak their queries.
  - **Text-to-Speech**: Manual audio playback for advice in both languages.

## 🛠️ Technical Stack

- **Backend**: FastAPI (Python)
- **LLM Engine**: Llama-3.2-3B-Instruct (via Hugging Face)
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`)
- **Database**: MongoDB (Conversation History)
- **Frontend**: Vanilla HTML5, CSS3, JavaScript

## 🏗️ Architecture & Pipeline

1. **Ingestion**: The PDF guide is extracted and chunked into semantic vectors stored in FAISS.
2. **Retrieval**: User queries trigger a semantic search in FAISS for expert context.
3. **Augmentation**: 
   - Weather keywords trigger a GPS-based lookup.
   - Price keywords trigger an Agmarknet API call.
4. **Generation**: Llama-3.2 processes the expert chunks + Live API data to generate a concise, action-oriented bilingual response.

## 📋 Setup & Installation

### 1. Environment Variables
Create a `.env` file in the root directory:
```env
HUGGINGFACE_API_KEY=your_hf_key
HF_GEMINI_MODEL=meta-llama/Llama-3.2-3B-Instruct
MONGO_URI=mongodb://localhost:27017/agrobot
AGMARKNET_API_KEY=your_datagov_key
OPENWEATHER_API_KEY=your_openweather_key
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Run the Application
```powershell
python main_server.py
```
Visit `http://localhost:8000` to interact with AgroBot.

## 📄 Datasets
- **Expert PDF**: Localized tomato cultivation guide.
- **Live Streams**: Real-time JSON data from government and meteorological APIs.

---
*Developed as a technical solution for precision agriculture.*
