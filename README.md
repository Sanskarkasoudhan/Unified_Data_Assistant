# Unified Data Assistant

📊 **Unified Data Assistant** is a comprehensive tool designed to process, analyze, and query data from multiple sources, including CSV files, Excel files, and PDFs. It leverages advanced technologies like **Retrieval-Augmented Generation (RAG), Chroma, and FAISS** to provide intelligent insights and seamless querying across interrelated datasets.

## Features

### Upload and Process Data
- Upload individual files or folders containing multiple CSV files.
- Automatically infer relationships between tables (e.g., foreign key relationships).
- Store data in an SQLite database for efficient querying.

### Natural Language Querying
- Ask questions in plain English and retrieve answers from the database.
- Supports queries across interrelated tables using inferred relationships.
- Leverages Retrieval-Augmented Generation (RAG) for document-based queries.

### Visualization
- Dynamically generate visualizations based on query results.
- Supports custom visualization scripts.

### File Types Supported
- **CSV**: Process and store CSV files as database tables.
- **Excel**: Process `.xlsx` and `.xls` files.
- **PDF**: Extract and analyze text from PDF documents.

### Advanced Technologies
- **FAISS**: Efficient vector search for document embeddings.
- **Chroma**: Vector database for managing embeddings and retrieval.
- **Google Generative AI (Gemini API)**: Advanced natural language understanding.
- **LangChain**: Framework for building language model-powered applications.

## Tech Stack

### Backend
- **Python**: Core programming language.
- **SQLite**: Lightweight database for structured data storage.
- **LangChain**: Framework for natural language processing and querying.
- **FAISS**: Vector similarity search for document embeddings.
- **Chroma**: Vector database for embedding storage and retrieval.

### Frontend
- **Streamlit**: Interactive UI for file uploads, querying, and visualization.

### APIs
- **Google Generative AI (Gemini API)**: For advanced natural language understanding and embedding generation.

### Libraries
- **PyPDF2**: For extracting text from PDF files.
- **Pandas**: For data manipulation and processing.
- **Matplotlib**: For generating visualizations.
- **OpenAI Tools**: For SQL-based natural language queries.

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/your-username/Unified-Data-Assistant.git
cd Unified-Data-Assistant
```

### 2. Set Up a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure API Keys
Add your Google Generative AI (Gemini API) key to the `config.py` file:
```python
API_KEY = "your-gemini-api-key"
```

### 5. Run the Application
```sh
streamlit run app.py
```

## Usage

### 1. Upload Data
- Navigate to the **Upload** tab.
- Upload individual files or a folder containing multiple CSV files.
- The system will process the files, infer relationships, and store them in the SQLite database.

### 2. Query Data
- Navigate to the **Query** tab.
- Select the data source (e.g., Document Store or SQL Database).
- Enter your question in natural language (e.g., *"Show me all orders placed by customers in 2023"*).
- View the results and any generated visualizations.

### 3. Overview
- Navigate to the **Overview** tab to see a summary of uploaded data and inferred relationships.

## Advanced Features

### 1. Retrieval-Augmented Generation (RAG)
- Combines document retrieval with generative AI to answer complex queries.
- Uses embeddings stored in FAISS or Chroma for efficient retrieval.

### 2. Relationship Inference
- Automatically detects relationships between tables (e.g., foreign keys).
- Enables seamless querying across interrelated datasets.

### 3. Visualization
- Dynamically generates visualizations based on query results.
- Supports custom visualization scripts for advanced use cases.

## Contact
For questions or support, please contact:

- **Name**: Sanskar
- **Email**: indiansanskar2000@gmail.com
- **GitHub**: https://github.com/Sanskarkasoudhan

---

*Let me know if you need further customization or additional details!* 🚀

