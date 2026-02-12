import os
from chatbot_rag.rag_pipeline import setup_rag, load_rag, answer_question
from chatbot_rag.config import INDEX_PATH, CHUNKS_PATH

def main():
    print("--- AgroBot CLI ---")
    
    # Initialize RAG
    if os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH):
        load_rag()
    else:
        setup_rag()
    
    print("\nAgroBot is ready! Type 'exit' or 'quit' to stop.")
    
    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:
            break
        
        if not query.strip():
            continue
            
        print("AgroBot: Thinking...")
        response = answer_question(query)
        print(f"AgroBot: {response}")

if __name__ == "__main__":
    main()
