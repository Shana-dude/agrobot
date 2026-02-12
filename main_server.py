from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from chatbot_rag.routes import router
from chatbot_rag.rag_pipeline import setup_rag, load_rag
from chatbot_rag.config import INDEX_PATH, CHUNKS_PATH
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

# Initialize RAG: Load if exists, otherwise build
if os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH):
    load_rag()
else:
    setup_rag()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_server:app", host="0.0.0.0", port=8000, reload=True)
