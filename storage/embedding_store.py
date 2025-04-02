# import os
# import pickle
# import numpy as np
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from google.generativeai import configure, embed_content
# from config import GEMINI_API_KEY

# # Configure Gemini API
# configure(api_key=GEMINI_API_KEY)

# # Set up embedding model
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # Directory to store FAISS indices
# FAISS_INDEX_DIR = "./faiss_indices"
# os.makedirs(FAISS_INDEX_DIR, exist_ok=True)

# # Documents memory store
# documents_store = {}

# def get_index_path(doc_name):
#     """Get the path to the FAISS index for a document."""
#     return os.path.join(FAISS_INDEX_DIR, f"{doc_name}.faiss")

# def get_store_path(doc_name):
#     """Get the path to the document store for a document."""
#     return os.path.join(FAISS_INDEX_DIR, f"{doc_name}.pkl")

# def check_existing_embeddings(doc_name):
#     """Checks if embeddings already exist for a given document."""
#     return os.path.exists(get_index_path(doc_name))

# def store_embeddings(text_chunks, doc_name, chunk_size=1000):
#     """Stores embeddings for a document in FAISS, only if not already stored."""
    
#     # Check if embeddings for this document already exist
#     if check_existing_embeddings(doc_name):
#         print(f"✅ Embeddings for '{doc_name}' already exist. Skipping embedding process.")
#         return "Embeddings already exist"

#     # Filter out empty chunks
#     text_chunks = [chunk.strip() for chunk in text_chunks if chunk.strip()]

#     if not text_chunks:
#         print(f"⚠️ No valid text chunks found for '{doc_name}'. Skipping embedding.")
#         return "No valid text chunks found"

#     try:
#         # Create metadata for each chunk
#         metadatas = [{"source": doc_name, "chunk_id": i} for i in range(len(text_chunks))]
        
#         # Create FAISS index
#         vectorstore = FAISS.from_texts(text_chunks, embeddings, metadatas=metadatas)
        
#         # Save the index
#         vectorstore.save_local(get_index_path(doc_name))
        
#         # Store the original text chunks for retrieval
#         documents_store[doc_name] = text_chunks
#         with open(get_store_path(doc_name), 'wb') as f:
#             pickle.dump(text_chunks, f)
            
#         print(f"✅ Successfully stored embeddings for '{doc_name}'.")
#         return "Embeddings created successfully"
#     except Exception as e:
#         print(f"❌ Error storing embeddings: {e}")
#         return f"Error: {str(e)}"

# def retrieve_relevant_text(query, limit=3):
#     """Retrieves relevant text chunks from FAISS indices based on query."""
#     try:
#         # Get all document indices
#         all_docs = list_embedded_documents()
        
#         if not all_docs:
#             return [], []
        
#         # Search across all indices
#         results = []
#         sources = []
        
#         for doc_name in all_docs:
#             if os.path.exists(get_index_path(doc_name)):
#                 # Load the index
#                 vectorstore = FAISS.load_local(get_index_path(doc_name), embeddings,allow_dangerous_deserialization=True)
                
#                 # Load the document store
#                 if os.path.exists(get_store_path(doc_name)):
#                     with open(get_store_path(doc_name), 'rb') as f:
#                         text_chunks = pickle.load(f)
#                 else:
#                     continue
                
#                 # Search for similar chunks
#                 docs = vectorstore.similarity_search(query, k=limit)
                
#                 for doc in docs:
#                     chunk_id = doc.metadata.get("chunk_id", -1)
#                     if chunk_id >= 0 and chunk_id < len(text_chunks):
#                         results.append(text_chunks[chunk_id])
#                         sources.append(doc_name)
        
#         # Return the top results
#         return results[:limit], sources[:limit]
        
#     except Exception as e:
#         print(f"⚠️ Error retrieving text: {e}")
#         return [], []

# def list_embedded_documents():
#     """List all documents that have embeddings."""
#     docs = []
#     for file in os.listdir(FAISS_INDEX_DIR):
#         if file.endswith(".faiss"):
#             docs.append(file[:-6])  # Remove .faiss extension
#     return docs

# import os
# import pickle
# import numpy as np
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from google.generativeai import configure, embed_content
# from config import GEMINI_API_KEY

# # Configure Gemini API
# configure(api_key=GEMINI_API_KEY)

# # Set up embedding model
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # Directory to store FAISS indices
# FAISS_INDEX_DIR = "./faiss_indices"
# os.makedirs(FAISS_INDEX_DIR, exist_ok=True)

# # Folder-specific indices directory
# # FOLDER_INDICES_DIR = "./folder_indices"
# # os.makedirs(FOLDER_INDICES_DIR, exist_ok=True)

# # Documents memory store
# documents_store = {}

# def get_index_path(doc_name, folder_name=None):
#     """Get the path to the FAISS index for a document."""
#     if folder_name:
#         # Create folder directory if it doesn't exist
#         folder_dir = os.path.join(FOLDER_INDICES_DIR, folder_name)
#         os.makedirs(folder_dir, exist_ok=True)
#         return os.path.join(folder_dir, f"{doc_name}.faiss")
#     return os.path.join(FAISS_INDEX_DIR, f"{doc_name}.faiss")

# def get_store_path(doc_name, folder_name=None):
#     """Get the path to the document store for a document."""
#     if folder_name:
#         folder_dir = os.path.join(FOLDER_INDICES_DIR, folder_name)
#         os.makedirs(folder_dir, exist_ok=True)
#         return os.path.join(folder_dir, f"{doc_name}.pkl")
#     return os.path.join(FAISS_INDEX_DIR, f"{doc_name}.pkl")

# def check_existing_embeddings(doc_name, folder_name=None):
#     """Checks if embeddings already exist for a given document."""
#     return os.path.exists(get_index_path(doc_name, folder_name))

# def store_embeddings(text_chunks, doc_name, folder_name=None, chunk_size=1000):
#     """Stores embeddings for a document in FAISS, only if not already stored."""
    
#     # Check if embeddings for this document already exist
#     if check_existing_embeddings(doc_name, folder_name):
#         print(f"✅ Embeddings for '{doc_name}' already exist. Skipping embedding process.")
#         return "Embeddings already exist"

#     # Filter out empty chunks
#     text_chunks = [chunk.strip() for chunk in text_chunks if chunk.strip()]

#     if not text_chunks:
#         print(f"⚠️ No valid text chunks found for '{doc_name}'. Skipping embedding.")
#         return "No valid text chunks found"

#     try:
#         # Create metadata for each chunk, including folder information if provided
#         if folder_name:
#             metadatas = [{"source": doc_name, "chunk_id": i, "folder": folder_name} for i in range(len(text_chunks))]
#         else:
#             metadatas = [{"source": doc_name, "chunk_id": i} for i in range(len(text_chunks))]
        
#         # Create FAISS index
#         vectorstore = FAISS.from_texts(text_chunks, embeddings, metadatas=metadatas)
        
#         # Save the index
#         vectorstore.save_local(get_index_path(doc_name, folder_name))
        
#         # Store the original text chunks for retrieval
#         documents_store[doc_name] = text_chunks
#         with open(get_store_path(doc_name, folder_name), 'wb') as f:
#             pickle.dump(text_chunks, f)
            
#         print(f"✅ Successfully stored embeddings for '{doc_name}'{' in folder ' + folder_name if folder_name else ''}.")
#         return "Embeddings created successfully"
#     except Exception as e:
#         print(f"❌ Error storing embeddings: {e}")
#         return f"Error: {str(e)}"

# def retrieve_relevant_text(query, limit=3, folder_name=None):
#     """Retrieves relevant text chunks from FAISS indices based on query."""
#     try:
#         # Get all document indices
#         if folder_name:
#             all_docs = list_embedded_documents(folder_name)
#         else:
#             all_docs = list_embedded_documents()
        
#         if not all_docs:
#             return [], []
        
#         # Search across all indices
#         results = []
#         sources = []
        
#         for doc_name in all_docs:
#             index_path = get_index_path(doc_name, folder_name)
#             store_path = get_store_path(doc_name, folder_name)
            
#             if os.path.exists(index_path):
#                 # Load the index
#                 vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
                
#                 # Load the document store
#                 if os.path.exists(store_path):
#                     with open(store_path, 'rb') as f:
#                         text_chunks = pickle.load(f)
#                 else:
#                     continue
                
#                 # Search for similar chunks
#                 docs = vectorstore.similarity_search(query, k=limit)
                
#                 for doc in docs:
#                     chunk_id = doc.metadata.get("chunk_id", -1)
#                     if chunk_id >= 0 and chunk_id < len(text_chunks):
#                         results.append(text_chunks[chunk_id])
#                         source_name = doc_name
#                         if folder_name:
#                             source_name = f"{folder_name}/{doc_name}"
#                         sources.append(source_name)
        
#         # Return the top results
#         return results[:limit], sources[:limit]
        
#     except Exception as e:
#         print(f"⚠️ Error retrieving text: {e}")
#         return [], []

# def list_embedded_documents(folder_name=None):
#     """List all documents that have embeddings."""
#     docs = []
    
#     if folder_name:
#         folder_dir = os.path.join(FOLDER_INDICES_DIR, folder_name)
#         if not os.path.exists(folder_dir):
#             return docs
            
#         for file in os.listdir(folder_dir):
#             if file.endswith(".faiss"):
#                 docs.append(file[:-6])  # Remove .faiss extension
#     else:
#         for file in os.listdir(FAISS_INDEX_DIR):
#             if file.endswith(".faiss"):
#                 docs.append(file[:-6])  # Remove .faiss extension
                
#     return docs

# def list_folders():
#     """List all folders with embedded documents."""
#     if not os.path.exists(FOLDER_INDICES_DIR):
#         return []
        
#     return [folder for folder in os.listdir(FOLDER_INDICES_DIR) 
#             if os.path.isdir(os.path.join(FOLDER_INDICES_DIR, folder))]

# def get_embeddings_for_folder(folder_name):
#     """
#     Get information about embeddings in a specific folder.
    
#     Args:
#         folder_name (str): Name of the folder
        
#     Returns:
#         dict: Information about documents and chunks in the folder
#     """
#     if not folder_name or not os.path.exists(os.path.join(FOLDER_INDICES_DIR, folder_name)):
#         return {"status": "error", "message": f"Folder '{folder_name}' not found"}
    
#     docs = list_embedded_documents(folder_name)
    
#     if not docs:
#         return {"status": "empty", "message": f"No embedded documents in folder '{folder_name}'"}
    
#     documents_info = []
#     total_chunks = 0
    
#     for doc_name in docs:
#         store_path = get_store_path(doc_name, folder_name)
#         if os.path.exists(store_path):
#             with open(store_path, 'rb') as f:
#                 text_chunks = pickle.load(f)
#                 num_chunks = len(text_chunks) if text_chunks else 0
#                 total_chunks += num_chunks
#                 documents_info.append({
#                     "name": doc_name,
#                     "chunks": num_chunks
#                 })
    
#     return {
#         "status": "success",
#         "folder": folder_name,
#         "documents": documents_info,
#         "total_docs": len(docs),
#         "total_chunks": total_chunks
#     }

# import os
# import pickle
# import numpy as np
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from google.generativeai import configure, embed_content
# from config import GEMINI_API_KEY

# # Configure Gemini API
# configure(api_key=GEMINI_API_KEY)

# # Set up embedding model
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # Directory to store FAISS indices
# FAISS_INDEX_DIR = "./faiss_indices"
# os.makedirs(FAISS_INDEX_DIR, exist_ok=True)

# # Documents memory store
# documents_store = {}

# def get_index_path(doc_name):
#     """Get the path to the FAISS index for a document."""
#     return os.path.join(FAISS_INDEX_DIR, f"{doc_name}.faiss")

# def get_store_path(doc_name):
#     """Get the path to the document store for a document."""
#     return os.path.join(FAISS_INDEX_DIR, f"{doc_name}.pkl")

# def check_existing_embeddings(doc_name):
#     """Checks if embeddings already exist for a given document."""
#     return os.path.exists(get_index_path(doc_name))

# def store_embeddings(text_chunks, doc_name, chunk_size=1000):
#     """Stores embeddings for a document in FAISS, only if not already stored."""
    
#     # Check if embeddings for this document already exist
#     if check_existing_embeddings(doc_name):
#         print(f"✅ Embeddings for '{doc_name}' already exist. Skipping embedding process.")
#         return "Embeddings already exist"

#     # Filter out empty chunks
#     text_chunks = [chunk.strip() for chunk in text_chunks if chunk.strip()]

#     if not text_chunks:
#         print(f"⚠️ No valid text chunks found for '{doc_name}'. Skipping embedding.")
#         return "No valid text chunks found"

#     try:
#         # Create metadata for each chunk
#         metadatas = [{"source": doc_name, "chunk_id": i} for i in range(len(text_chunks))]
        
#         # Create FAISS index
#         vectorstore = FAISS.from_texts(text_chunks, embeddings, metadatas=metadatas)
        
#         # Save the index
#         vectorstore.save_local(get_index_path(doc_name))
        
#         # Store the original text chunks for retrieval
#         documents_store[doc_name] = text_chunks
#         with open(get_store_path(doc_name), 'wb') as f:
#             pickle.dump(text_chunks, f)
            
#         print(f"✅ Successfully stored embeddings for '{doc_name}'.")
#         return "Embeddings created successfully"
#     except Exception as e:
#         print(f"❌ Error storing embeddings: {e}")
#         return f"Error: {str(e)}"

# def retrieve_relevant_text(query, limit=3):
#     """Retrieves relevant text chunks from FAISS indices based on query."""
#     try:
#         # Get all document indices
#         all_docs = list_embedded_documents()
        
#         if not all_docs:
#             return [], []
        
#         # Search across all indices
#         results = []
#         sources = []
        
#         for doc_name in all_docs:
#             index_path = get_index_path(doc_name)
#             store_path = get_store_path(doc_name)
            
#             if os.path.exists(index_path):
#                 # Load the index
#                 vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
                
#                 # Load the document store
#                 if os.path.exists(store_path):
#                     with open(store_path, 'rb') as f:
#                         text_chunks = pickle.load(f)
#                 else:
#                     continue
                
#                 # Search for similar chunks
#                 docs = vectorstore.similarity_search(query, k=limit)
                
#                 for doc in docs:
#                     chunk_id = doc.metadata.get("chunk_id", -1)
#                     if chunk_id >= 0 and chunk_id < len(text_chunks):
#                         results.append(text_chunks[chunk_id])
#                         sources.append(doc_name)
        
#         # Return the top results
#         return results[:limit], sources[:limit]
        
#     except Exception as e:
#         print(f"⚠️ Error retrieving text: {e}")
#         return [], []

# def list_embedded_documents():
#     """List all documents that have embeddings."""
#     docs = []
    
#     for file in os.listdir(FAISS_INDEX_DIR):
#         if file.endswith(".faiss"):
#             docs.append(file[:-6])  # Remove .faiss extension
                
#     return docs

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