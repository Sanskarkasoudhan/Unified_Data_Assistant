# import google.generativeai as genai
# import os
# from storage.embedding_store import retrieve_relevant_text
# from config import GEMINI_API_KEY, TEMP_VIZ_FILE

# # Configure Gemini API
# genai.configure(api_key=GEMINI_API_KEY)

# def generate_answer_with_visualization(query):
#     """Generates an answer along with Matplotlib code for visualization.""" 
    
#     # Retrieve relevant text from ChromaDB
#     relevant_texts, sources = retrieve_relevant_text(query)

#     if not relevant_texts:
#         return "No relevant information found in the documents.", "", False

#     # Prepare prompt with retrieved context
#     context = "\n".join(relevant_texts)
#     sources_text = ", ".join(set(sources))
    
#     prompt = f"""
#     Based on the following information from {sources_text}:
    
#     {context}
    
#     Question: {query}
    
#     Answer the question first in text.
#     Then, if the answer contains numerical trends, generate **only** valid Python Matplotlib code for visualization.
    
#     **Matplotlib code rules:**
#     - Use `matplotlib.pyplot`
#     - Define a figure and axis using `fig, ax = plt.subplots()`
#     - Label axes, set titles, and include a legend if necessary
#     - **No explanations—return only the code**
#     - End with `plt.show()`
    
#     Ensure the code is properly formatted within triple backticks.
#     """

#     # Use Gemini AI to generate a response
#     model = genai.GenerativeModel("gemini-2.0-flash")
#     response = model.generate_content(prompt)

#     if hasattr(response, "text"):
#         response_text = response.text
#     else:
#         response_text = response.candidates[0].content  # Fallback for response format

#     # Extract answer and Matplotlib code
#     parts = response_text.split("```")
#     answer = parts[0].strip()
    
#     # Extract and clean the Matplotlib code
#     if len(parts) > 1:
#         matplotlib_code = parts[1].replace("python", "").strip()
        
#         # Ensure `plt.show()` is included
#         if "plt.show()" not in matplotlib_code:
#             matplotlib_code += "\nplt.show()"
            
#         # Write Matplotlib code to a temp file if not empty
#         with open(TEMP_VIZ_FILE, "w", encoding="utf-8") as f:
#             f.write("import streamlit as st\n")
#             f.write("import matplotlib.pyplot as plt\n\n")  
#             f.write("st.title('Visualization')\n\n")
#             f.write("code_from_gemini = '''\n")  
#             f.write(matplotlib_code)
#             f.write("\n'''\n\n")  
#             f.write("exec(code_from_gemini, globals())\n")
#             f.write("st.pyplot(fig)\n")

#         # Write Matplotlib code to a separate visualization file
#         with open("visualization.py", "w", encoding="utf-8") as f:
#             f.write(matplotlib_code)

#         # Example of writing to a file with UTF-8 encoding
#         with open("output_file.txt", "w", encoding="utf-8") as f:
#             f.write(answer)
            
#         return answer, TEMP_VIZ_FILE, True
#     else:
#         return answer, "", False  # No visualization

# import google.generativeai as genai
# import os
# from storage.embedding_store import retrieve_relevant_text, list_folders, get_embeddings_for_folder
# from config import GEMINI_API_KEY, TEMP_VIZ_FILE

# # Configure Gemini API
# genai.configure(api_key=GEMINI_API_KEY)

# def generate_answer_with_visualization(query):
#     """Generates an answer along with Matplotlib code for visualization.""" 
    
#     # Retrieve relevant text from FAISS
#     relevant_texts, sources = retrieve_relevant_text(query)

#     if not relevant_texts:
#         return "No relevant information found in the documents.", "", False

#     # Prepare prompt with retrieved context
#     context = "\n".join(relevant_texts)
#     sources_text = ", ".join(set(sources))
    
#     prompt = f"""
#     Based on the following information from {sources_text}:
    
#     {context}
    
#     Question: {query}
    
#     Answer the question first in text.
#     Then, if the answer contains numerical trends, generate **only** valid Python Matplotlib code for visualization.
    
#     **Matplotlib code rules:**
#     - Use `matplotlib.pyplot`
#     - Define a figure and axis using `fig, ax = plt.subplots()`
#     - Label axes, set titles, and include a legend if necessary
#     - **No explanations—return only the code**
#     - End with `plt.show()`
    
#     Ensure the code is properly formatted within triple backticks.
#     """

#     # Use Gemini AI to generate a response
#     model = genai.GenerativeModel("gemini-2.0-flash")
#     response = model.generate_content(prompt)

#     if hasattr(response, "text"):
#         response_text = response.text
#     else:
#         response_text = response.candidates[0].content  # Fallback for response format

#     # Extract answer and Matplotlib code
#     parts = response_text.split("```")
#     answer = parts[0].strip()
    
#     # Extract and clean the Matplotlib code
#     if len(parts) > 1:
#         matplotlib_code = parts[1].replace("python", "").strip()
        
#         # Ensure `plt.show()` is included
#         if "plt.show()" not in matplotlib_code:
#             matplotlib_code += "\nplt.show()"
            
#         # Write Matplotlib code to a temp file if not empty
#         with open(TEMP_VIZ_FILE, "w", encoding="utf-8") as f:
#             f.write("import streamlit as st\n")
#             f.write("import matplotlib.pyplot as plt\n\n")  
#             f.write("st.title('Visualization')\n\n")
#             f.write("code_from_gemini = '''\n")  
#             f.write(matplotlib_code)
#             f.write("\n'''\n\n")  
#             f.write("exec(code_from_gemini, globals())\n")
#             f.write("st.pyplot(fig)\n")

#         # Write Matplotlib code to a separate visualization file
#         with open("visualization.py", "w", encoding="utf-8") as f:
#             f.write(matplotlib_code)

#         # Example of writing to a file with UTF-8 encoding
#         with open("output_file.txt", "w", encoding="utf-8") as f:
#             f.write(answer)
            
#         return answer, TEMP_VIZ_FILE, True
#     else:
#         return answer, "", False  # No visualization

# def generate_answer_from_folder(query, folder_name):
#     """
#     Generate an answer based on documents in a specific folder
    
#     Args:
#         query (str): The user's query
#         folder_name (str): Name of the folder
        
#     Returns:
#         str: The generated answer
#         str: Path to visualization file if any
#         bool: Whether visualization exists
#     """
#     # Retrieve relevant text from FAISS for the specific folder
#     relevant_texts, sources = retrieve_relevant_text(query, limit=5, folder_name=folder_name)

#     if not relevant_texts:
#         return f"No relevant information found in the folder '{folder_name}'.", "", False

#     # Prepare prompt with retrieved context
#     context = "\n".join(relevant_texts)
#     sources_text = ", ".join(set(sources))
    
#     prompt = f"""
#     Based on the following information from folder '{folder_name}' (sources: {sources_text}):
    
#     {context}
    
#     Question: {query}
    
#     Answer the question first in text.
#     Then, if the answer contains numerical trends, generate **only** valid Python Matplotlib code for visualization.
    
#     **Matplotlib code rules:**
#     - Use `matplotlib.pyplot`
#     - Define a figure and axis using `fig, ax = plt.subplots()`
#     - Label axes, set titles, and include a legend if necessary
#     - **No explanations—return only the code**
#     - End with `plt.show()`
    
#     Ensure the code is properly formatted within triple backticks.
#     """

#     # Use Gemini AI to generate a response
#     model = genai.GenerativeModel("gemini-2.0-flash")
#     response = model.generate_content(prompt)

#     if hasattr(response, "text"):
#         response_text = response.text
#     else:
#         response_text = response.candidates[0].content  # Fallback for response format

#     # Extract answer and Matplotlib code
#     parts = response_text.split("```")
#     answer = parts[0].strip()
    
#     # Add source information to the answer
#     answer += f"\n\nSources from folder '{folder_name}':"
#     unique_sources = list(set(sources))
#     for src in unique_sources[:5]:  # Limit to 5 sources
#         answer += f"\n- {src}"
    
#     # Extract and clean the Matplotlib code
#     if len(parts) > 1:
#         matplotlib_code = parts[1].replace("python", "").strip()
        
#         # Ensure `plt.show()` is included
#         if "plt.show()" not in matplotlib_code:
#             matplotlib_code += "\nplt.show()"
            
#         # Create folder-specific visualization file path
#         viz_file = f"viz_{folder_name.replace(' ', '_')}.py"
            
#         # Write Matplotlib code to a temp file if not empty
#         with open(viz_file, "w", encoding="utf-8") as f:
#             f.write("import streamlit as st\n")
#             f.write("import matplotlib.pyplot as plt\n\n")  
#             f.write(f"st.title('Visualization from {folder_name}')\n\n")
#             f.write("code_from_gemini = '''\n")  
#             f.write(matplotlib_code)
#             f.write("\n'''\n\n")  
#             f.write("exec(code_from_gemini, globals())\n")
#             f.write("st.pyplot(fig)\n")
            
#         return answer, viz_file, True
#     else:
#         return answer, "", False  # No visualization

# def query_across_all_folders(query, limit_per_folder=3):
#     """
#     Query across all folders and return consolidated results
    
#     Args:
#         query (str): The user's query
#         limit_per_folder (int): Maximum results per folder
        
#     Returns:
#         dict: Results organized by folder
#     """
#     folders = list_folders()
    
#     if not folders:
#         return {"status": "error", "message": "No folders found with embedded documents"}
    
#     results = {}
    
#     for folder in folders:
#         answer, viz_file, has_viz = generate_answer_from_folder(query, folder)
#         results[folder] = {
#             "answer": answer,
#             "visualization": viz_file if has_viz else None,
#             "has_visualization": has_viz
#         }
    
#     return {
#         "status": "success",
#         "folders": folders,
#         "results": results
#     }

# import google.generativeai as genai
# import os
# from storage.embedding_store import retrieve_relevant_text, list_embedded_documents
# from config import GEMINI_API_KEY, TEMP_VIZ_FILE

# # Configure Gemini API
# genai.configure(api_key=GEMINI_API_KEY)

# def generate_answer_with_visualization(query):
#     """Generates an answer along with Matplotlib code for visualization.""" 
    
#     # Retrieve relevant text from FAISS
#     relevant_texts, sources = retrieve_relevant_text(query)

#     if not relevant_texts:
#         return "No relevant information found in the documents.", "", False

#     # Prepare prompt with retrieved context
#     context = "\n".join(relevant_texts)
#     sources_text = ", ".join(set(sources))
    
#     prompt = f"""
#     Based on the following information from {sources_text}:
    
#     {context}
    
#     Question: {query}
    
#     Answer the question first in text.
#     Then, if the answer contains numerical trends, generate **only** valid Python Matplotlib code for visualization.
    
#     **Matplotlib code rules:**
#     - Use `matplotlib.pyplot`
#     - Define a figure and axis using `fig, ax = plt.subplots()`
#     - Label axes, set titles, and include a legend if necessary
#     - **No explanations—return only the code**
#     - End with `plt.show()`
    
#     Ensure the code is properly formatted within triple backticks.
#     """

#     # Use Gemini AI to generate a response
#     model = genai.GenerativeModel("gemini-2.0-flash")
#     response = model.generate_content(prompt)

#     if hasattr(response, "text"):
#         response_text = response.text
#     else:
#         response_text = response.candidates[0].content  # Fallback for response format

#     # Extract answer and Matplotlib code
#     parts = response_text.split("```")
#     answer = parts[0].strip()
    
#     # Add source information to the answer
#     answer += f"\n\nSources:"
#     unique_sources = list(set(sources))
#     for src in unique_sources[:5]:  # Limit to 5 sources
#         answer += f"\n- {src}"
    
#     # Extract and clean the Matplotlib code
#     if len(parts) > 1:
#         matplotlib_code = parts[1].replace("python", "").strip()
        
#         # Ensure `plt.show()` is included
#         if "plt.show()" not in matplotlib_code:
#             matplotlib_code += "\nplt.show()"
            
#         # Write Matplotlib code to a temp file if not empty
#         with open(TEMP_VIZ_FILE, "w", encoding="utf-8") as f:
#             f.write("import streamlit as st\n")
#             f.write("import matplotlib.pyplot as plt\n\n")  
#             f.write("st.title('Visualization')\n\n")
#             f.write("code_from_gemini = '''\n")  
#             f.write(matplotlib_code)
#             f.write("\n'''\n\n")  
#             f.write("exec(code_from_gemini, globals())\n")
#             f.write("st.pyplot(fig)\n")

#         # Write Matplotlib code to a separate visualization file
#         with open("visualization.py", "w", encoding="utf-8") as f:
#             f.write(matplotlib_code)

#         # Example of writing to a file with UTF-8 encoding
#         with open("output_file.txt", "w", encoding="utf-8") as f:
#             f.write(answer)
            
#         return answer, TEMP_VIZ_FILE, True
#     else:
#         return answer, "", False  # No visualization

import google.generativeai as genai
import os
from storage.embedding_store import retrieve_relevant_text, list_embedded_documents
from config import GEMINI_API_KEY, TEMP_VIZ_FILE

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def retrieve_relevant_text_from_specific_doc(query, doc_name, limit=3):
    """Retrieves relevant text chunks from a specific document."""
    # Implementation will be added in the embedding_store.py file
    # For now, this is a placeholder
    from storage.embedding_store import retrieve_relevant_text_from_doc
    return retrieve_relevant_text_from_doc(query, doc_name, limit)

def generate_answer_with_visualization(query, selected_doc=None):
    """Generates an answer along with Matplotlib code for visualization.
    
    Args:
        query (str): The user's query
        selected_doc (str, optional): A specific document to query. If None, query all docs.
    """
    
    # If a specific document is selected, only query that document
    if selected_doc:
        relevant_texts, sources = retrieve_relevant_text_from_specific_doc(query, selected_doc)
    else:
        # Retrieve relevant text from all documents in FAISS
        relevant_texts, sources = retrieve_relevant_text(query)

    if not relevant_texts:
        return "No relevant information found in the documents.", "", False

    # Prepare prompt with retrieved context
    context = "\n".join(relevant_texts)
    sources_text = ", ".join(set(sources))
    
    prompt = f"""
    Based on the following information from {sources_text}:
    
    {context}
    
    Question: {query}
    
    Answer the question first in text.
    Then, if the answer contains numerical trends, generate **only** valid Python Matplotlib code for visualization.
    
    **Matplotlib code rules:**
    - Use `matplotlib.pyplot`
    - Define a figure and axis using `fig, ax = plt.subplots()`
    - Label axes, set titles, and include a legend if necessary
    - **No explanations—return only the code**
    - End with `plt.show()`
    
    Ensure the code is properly formatted within triple backticks.
    """

    # Use Gemini AI to generate a response
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    if hasattr(response, "text"):
        response_text = response.text
    else:
        response_text = response.candidates[0].content  # Fallback for response format

    # Extract answer and Matplotlib code
    parts = response_text.split("```")
    answer = parts[0].strip()
    
    # Add source information to the answer
    answer += f"\n\nSources:"
    unique_sources = list(set(sources))
    for src in unique_sources[:5]:  # Limit to 5 sources
        answer += f"\n- {src}"
    
    # Extract and clean the Matplotlib code
    if len(parts) > 1:
        matplotlib_code = parts[1].replace("python", "").strip()
        
        # Ensure `plt.show()` is included
        if "plt.show()" not in matplotlib_code:
            matplotlib_code += "\nplt.show()"
            
        # Write Matplotlib code to a temp file if not empty
        with open(TEMP_VIZ_FILE, "w", encoding="utf-8") as f:
            f.write("import streamlit as st\n")
            f.write("import matplotlib.pyplot as plt\n\n")  
            f.write("st.title('Visualization')\n\n")
            f.write("code_from_gemini = '''\n")  
            f.write(matplotlib_code)
            f.write("\n'''\n\n")  
            f.write("exec(code_from_gemini, globals())\n")
            f.write("st.pyplot(fig)\n")

        # Write Matplotlib code to a separate visualization file
        with open("visualization.py", "w", encoding="utf-8") as f:
            f.write(matplotlib_code)

        # Example of writing to a file with UTF-8 encoding
        with open("output_file.txt", "w", encoding="utf-8") as f:
            f.write(answer)
            
        return answer, TEMP_VIZ_FILE, True
    else:
        return answer, "", False  # No visualization