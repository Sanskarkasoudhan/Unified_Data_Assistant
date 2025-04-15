📊 **Unified Data Assistant** is a comprehensive tool designed to process, analyze, and query data from multiple sources, including CSV files, Excel files, and PDFs. It leverages advanced technologies like Retrieval-Augmented Generation (RAG), Chroma, FAISS, SQLite, and LangChain SQL Agent to provide intelligent insights and seamless querying across interrelated datasets.

![Data Assistant Banner](https://via.placeholder.com/800x200)

## 🌟 Features

### Data Processing
- **Multiple File Types**: Process CSV, Excel (.xlsx, .xls), and PDF files
- **Smart Relationship Detection**: Automatically infer relationships between tables (e.g., foreign key relationships)
- **Dual Processing Pipeline**:
  - **PDF Pipeline**: Extract text → Chunk → Convert to vectors → Store in FAISS or Chroma vector database
  - **CSV/Excel Pipeline**: Process structured data → Store in SQLite database tables

### Intelligent Querying
- **Natural Language Interface**: Ask questions in plain English
- **Cross-Table Queries**: Seamlessly query across related datasets
- **RAG Technology**: Retrieve relevant document snippets to augment AI responses
- **LangChain SQL Agent**: Convert natural language to efficient SQL queries

### Visualization
- **Dynamic Charts**: Generate visualizations based on query results
- **Custom Visualization Scripts**: Support for advanced visualization needs

## 🛠️ Tech Stack

### Backend
- **Python**: Core programming language
- **SQLite**: Lightweight database for structured data
- **LangChain**: Framework for natural language processing
- **FAISS/Chroma**: Vector storage and similarity search
- **Google Generative AI (Gemini API)**: Advanced language understanding

### Frontend
- **Streamlit**: Interactive UI for file uploads, querying, and visualization

## 📋 Prerequisites

- Python 3.8+
- Google Generative AI API key

## 🚀 Getting Started

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Unified-Data-Assistant.git
   cd Unified-Data-Assistant
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys:**
   Create a `config.py` file with your API key:
   ```python
   API_KEY = "your-gemini-api-key"
   ```

5. **Launch the application:**
   ```bash
   streamlit run app.py
   ```

## 🔍 Usage

### 1. Upload Data
- Navigate to the **Upload** tab
- Upload individual files or entire folders
- The system processes files and stores them appropriately

### 2. Query Your Data
- Go to the **Query** tab
- Select data source (Document Store or SQL Database)
- Enter questions in natural language
- View results and visualizations

### 3. Data Overview
- Check the **Overview** tab for a summary of uploaded data and inferred relationships

## 📊 Example Queries

- "Show me all orders placed by customers in 2023"
- "What are the top 5 products by revenue?"
- "Summarize the key points from the annual report"
- "Show the relationship between customer age and purchase amount"

## 🗂️ Project Structure

```
Unified-Data-Assistant/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration file for API keys
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
├── data/                  # Storage for uploaded files
├── utils/
│   ├── database.py        # SQLite database operations
│   ├── pdf_processor.py   # PDF extraction and vector storage
│   ├── csv_processor.py   # CSV/Excel processing
│   ├── query_engine.py    # Natural language query processing
│   └── visualizer.py      # Data visualization tools
└── models/                # Model configurations and agents
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

- **Name**: Sanskar
- **Email**: indiansanskar2000@gmail.com
- **GitHub**: [Sanskarkasoudhan](https://github.com/Sanskarkasoudhan)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

*For questions or support, please open an issue or contact the author directly.*

