import os
import pickle
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from google.generativeai import configure, embed_content
from config import GEMINI_API_KEY

# Configure Gemini API
configure(api_key=GEMINI_API_KEY)

# Set up embedding model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Directory to store FAISS indices
FAISS_INDEX_DIR = "./faiss_indices"
os.makedirs(FAISS_INDEX_DIR, exist_ok=True)

# Documents memory store
documents_store = {}

def get_index_path(doc_name):
    """Get the path to the FAISS index for a document."""
    return os.path.join(FAISS_INDEX_DIR, f"{doc_name}.faiss")

def get_store_path(doc_name):
    """Get the path to the document store for a document."""
    return os.path.join(FAISS_INDEX_DIR, f"{doc_name}.pkl")

def check_existing_embeddings(doc_name):
    """Checks if embeddings already exist for a given document."""
    return os.path.exists(get_index_path(doc_name))

def store_embeddings(text_chunks, doc_name, chunk_size=1000):
    """Stores embeddings for a document in FAISS, only if not already stored."""
    
    # Check if embeddings for this document already exist
    if check_existing_embeddings(doc_name):
        print(f"✅ Embeddings for '{doc_name}' already exist. Skipping embedding process.")
        return "Embeddings already exist"

    # Filter out empty chunks
    text_chunks = [chunk.strip() for chunk in text_chunks if chunk.strip()]

    if not text_chunks:
        print(f"⚠️ No valid text chunks found for '{doc_name}'. Skipping embedding.")
        return "No valid text chunks found"

    try:
        # Create metadata for each chunk
        metadatas = [{"source": doc_name, "chunk_id": i} for i in range(len(text_chunks))]
        
        # Create FAISS index
        vectorstore = FAISS.from_texts(text_chunks, embeddings, metadatas=metadatas)
        
        # Save the index
        vectorstore.save_local(get_index_path(doc_name))
        
        # Store the original text chunks for retrieval
        documents_store[doc_name] = text_chunks
        with open(get_store_path(doc_name), 'wb') as f:
            pickle.dump(text_chunks, f)
            
        print(f"✅ Successfully stored embeddings for '{doc_name}'.")
        return "Embeddings created successfully"
    except Exception as e:
        print(f"❌ Error storing embeddings: {e}")
        return f"Error: {str(e)}"

def retrieve_relevant_text(query, limit=3):
    """Retrieves relevant text chunks from FAISS indices based on query."""
    try:
        # Get all document indices
        all_docs = list_embedded_documents()
        
        if not all_docs:
            return [], []
        
        # Search across all indices
        results = []
        sources = []
        
        for doc_name in all_docs:
            index_path = get_index_path(doc_name)
            store_path = get_store_path(doc_name)
            
            if os.path.exists(index_path):
                # Load the index
                vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
                
                # Load the document store
                if os.path.exists(store_path):
                    with open(store_path, 'rb') as f:
                        text_chunks = pickle.load(f)
                else:
                    continue
                
                # Search for similar chunks
                docs = vectorstore.similarity_search(query, k=limit)
                
                for doc in docs:
                    chunk_id = doc.metadata.get("chunk_id", -1)
                    if chunk_id >= 0 and chunk_id < len(text_chunks):
                        results.append(text_chunks[chunk_id])
                        sources.append(doc_name)
        
        # Return the top results
        return results[:limit], sources[:limit]
        
    except Exception as e:
        print(f"⚠️ Error retrieving text: {e}")
        return [], []

def retrieve_relevant_text_from_doc(query, doc_name, limit=3):
    """Retrieves relevant text chunks from a specific document."""
    try:
        # Check if document exists
        if not check_existing_embeddings(doc_name):
            print(f"⚠️ Document '{doc_name}' not found.")
            return [], []
        
        index_path = get_index_path(doc_name)
        store_path = get_store_path(doc_name)
        
        # Load the index
        vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        
        # Load the document store
        if os.path.exists(store_path):
            with open(store_path, 'rb') as f:
                text_chunks = pickle.load(f)
        else:
            print(f"⚠️ Document store for '{doc_name}' not found.")
            return [], []
        
        # Search for similar chunks
        docs = vectorstore.similarity_search(query, k=limit)
        
        results = []
        sources = []
        
        for doc in docs:
            chunk_id = doc.metadata.get("chunk_id", -1)
            if chunk_id >= 0 and chunk_id < len(text_chunks):
                results.append(text_chunks[chunk_id])
                sources.append(doc_name)
        
        return results, sources
        
    except Exception as e:
        print(f"⚠️ Error retrieving text from '{doc_name}': {e}")
        return [], []

def list_embedded_documents():
    """List all documents that have embeddings."""
    docs = []
    
    for file in os.listdir(FAISS_INDEX_DIR):
        if file.endswith(".faiss"):
            docs.append(file[:-6])  # Remove .faiss extension
                
    return docs