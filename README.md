📊 **Unified Data Assistant** is a comprehensive tool designed to process, analyze, and query data from multiple sources, including CSV files, Excel files, and PDFs. It leverages advanced technologies like *Retrieval-Augmented Generation (RAG)*, *Chroma*, *FAISS*, *SQLite*, and *LangChain SQL Agent* to provide intelligent insights and seamless querying across interrelated datasets.

## How It Works

The Unified Data Assistant operates through two main processing pipelines:

1. **PDF Processing Pipeline**:
   - When a PDF file is uploaded, it goes through the RAG pipeline
   - The system extracts all text from the PDF
   - Text is segmented into manageable chunks
   - These chunks are converted into vectors through vector embedding
   - Vectors are stored in either VectorDB or a FAISS local index
   - When a user asks a question, RAG retrieves the most relevant data to generate an answer

2. **CSV/XLSX Processing Pipeline**:
   - When CSV or Excel files are uploaded, the system processes the structured data
   - Data is stored in SQLite in proper table format with columns and rows
   - The system automatically identifies relationships between tables
   - LangChain SQL Agent is used to convert natural language queries into SQL
   - Query results are returned to the user, often with visualizations

## Features

### Upload and Process Data
- Upload individual files or folders containing multiple CSV files and PDF documents
- Once a PDF file is uploaded, it will store in VectorDB or FAISS local index
- If CSV or XLSX file, it automatically infers relationships between tables (e.g., foreign key relationships)
- Store data in an SQLite database for efficient querying

### Natural Language Querying
- Ask questions in plain English and retrieve answers from the database
- Supports queries across interrelated tables using inferred relationships
- Leverages **Retrieval-Augmented Generation (RAG)** for document-based queries
- Uses LangChain SQL Agent for efficient SQL-based querying

### Visualization
- Dynamically generate visualizations based on query results
- Supports custom visualization scripts

### File Types Supported
- **CSV**: Process and store CSV files as database tables
- **Excel**: Process `.xlsx` and `.xls` files
- **PDF**: Extract and analyze text from PDF documents

### Advanced Technologies
- **FAISS**: Efficient vector search for document embeddings
- **Chroma**: Vector database for managing embeddings and retrieval
- **Google Generative AI (Gemini API)**: Advanced natural language understanding
- **LangChain**: Framework for building language model-powered applications
- **LangChain SQL Agent**: Enables natural language to SQL query conversion for structured databases

## Tech Stack

### Backend
- **Python**: Core programming language
- **SQLite**: Lightweight database for structured data storage
- **LangChain**: Framework for natural language processing and querying
- **FAISS**: Vector similarity search for document embeddings
- **Chroma**: Vector database for embedding storage and retrieval
- **LangChain SQL Agent**: Enables SQL-based querying through natural language

### Frontend
- **Streamlit**: Interactive UI for file uploads, querying, and visualization

### APIs
- **Google Generative AI (Gemini API)**: For advanced natural language understanding and embedding generation

### Libraries
- **PyPDF2**: For extracting text from PDF files
- **Pandas**: For data manipulation and processing
- **Matplotlib**: For generating visualizations
- **OpenAI Tools**: For SQL-based natural language queries

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
- Navigate to the **Upload** tab
- Upload individual files or a folder containing multiple files
- For PDF files: The system will extract text, chunk it, create embeddings, and store them in a vector database
- For CSV/Excel files: The system will process tables, infer relationships, and store them in SQLite

### 2. Query Data
- Navigate to the **Query** tab
- Select the data source (e.g., Document Store or SQL Database)
- Enter your question in natural language (e.g., *"Show me all orders placed by customers in 2023"*)
- For PDF queries: The system will use RAG to find relevant document sections
- For structured data queries: LangChain SQL Agent will convert your question to SQL
- View the results and any generated visualizations

### 3. Overview
- Navigate to the **Overview** tab to see a summary of uploaded data and inferred relationships

## Example Queries

### For PDF Documents
- "What are the key findings in the annual report?"
- "Summarize the methodology section from the research paper"
- "Find information about market trends in the industry analysis"

### For CSV/Excel Data
- "Show me sales trends over the last 6 months"
- "What's the average order value by customer segment?"
- "Identify products with inventory below reorder point"
- "Compare performance across different regions"

## Advanced Features

### 1. Retrieval-Augmented Generation (RAG)
- Combines document retrieval with generative AI to answer complex queries
- Uses embeddings stored in FAISS or Chroma for efficient retrieval

### 2. Relationship Inference
- Automatically detects relationships between tables (e.g., foreign keys)
- Enables seamless querying across interrelated datasets

### 3. LangChain SQL Agent
- Converts natural language queries into SQL queries for structured data
- Enables querying large databases efficiently

### 4. Visualization
- Dynamically generates visualizations based on query results
- Supports custom visualization scripts for advanced use cases

## Contact
For questions or support, please contact:

- **Name**: Sanskar
- **Email**: indiansanskar2000@gmail.com
- **GitHub**: [Sanskarkasoudhan](https://github.com/Sanskarkasoudhan)

*For questions or support, please open an issue or contact the author directly.*
