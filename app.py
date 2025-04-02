import streamlit as st
import os
import pandas as pd
from io import BytesIO
import sys
import sqlite3

# Ensure paths are correct
sys.path.append(os.path.abspath("."))

# Import modules
from config import SQLITE_DB_PATH, CHROMA_DB_PATH
from processors.pdf_processor import extract_text_from_pdf, chunk_text
from processors.csv_processor import (
    process_csv_file, process_excel_file, 
    store_dataframe_to_sqlite, get_all_tables
)
from storage.embedding_store import (
    store_embeddings, check_existing_embeddings, 
    list_embedded_documents
)
from storage.sql_store import get_database_info, get_table_preview
from query.rag_query import generate_answer_with_visualization
from query.sql_query import execute_natural_language_query

# Page configuration
st.set_page_config(page_title="Unified Data Assistant", layout="wide", page_icon="📊")

# Create necessary directories
os.makedirs("uploaded_folders", exist_ok=True)
os.makedirs(os.path.dirname(SQLITE_DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(CHROMA_DB_PATH), exist_ok=True)

# Initialize session state
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Upload"
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'query_target' not in st.session_state:
    st.session_state.query_target = "auto"
if 'selected_doc' not in st.session_state:
    st.session_state.selected_doc = None
if 'selected_table' not in st.session_state:
    st.session_state.selected_table = None
if 'uploaded_folders' not in st.session_state:
    st.session_state.uploaded_folders = {}

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.button("Upload Data", on_click=lambda: setattr(st.session_state, 'active_tab', "Upload"))
st.sidebar.button("Query Data", on_click=lambda: setattr(st.session_state, 'active_tab', "Query"))
st.sidebar.button("Data Overview", on_click=lambda: setattr(st.session_state, 'active_tab', "Overview"))

st.sidebar.markdown("---")
st.sidebar.header("Data Sources")

# Display embedded documents
st.sidebar.subheader("Document Store")
embedded_docs = list_embedded_documents()
if embedded_docs:
    st.sidebar.write(f"Documents: {len(embedded_docs)}")
    with st.sidebar.expander("Show Documents"):
        for doc in embedded_docs:
            st.sidebar.write(f"- {doc}")
else:
    st.sidebar.write("No documents stored")

# Display SQL tables
st.sidebar.subheader("SQL Database")
sql_tables = get_all_tables(SQLITE_DB_PATH)
if sql_tables:
    st.sidebar.write(f"Tables: {len(sql_tables)}")
    with st.sidebar.expander("Show Tables"):
        for table in sql_tables:
            st.sidebar.write(f"- {table}")
else:
    st.sidebar.write("No tables stored")

# Functions for tab content
def upload_tab():
    st.header("Upload Data Files")
    
    # File upload section
    st.subheader("Upload Files or Folder Containing CSV Files")
    uploaded_files = st.file_uploader(
        "Upload PDF, CSV, or Excel files (or multiple CSV files as a folder)", 
        type=["pdf", "csv", "xlsx", "xls"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        folder_name = st.text_input("Enter a name for this folder (if uploading multiple CSV files):")
        
        if st.button("Process Files", key="process_files"):
            with st.spinner("Processing files..."):
                for uploaded_file in uploaded_files:
                    file_extension = uploaded_file.name.split('.')[-1].lower()
                    
                    # Process CSV files
                    if file_extension == 'csv':
                        st.info(f"Processing CSV: {uploaded_file.name}")
                        
                        # If folder name is provided, treat files as part of a folder
                        if folder_name:
                            folder_path = os.path.join("uploaded_folders", folder_name)
                            os.makedirs(folder_path, exist_ok=True)
                            file_path = os.path.join(folder_path, uploaded_file.name)
                            
                            # Save the file to the folder
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            
                            # Process CSV file using the file path
                            df, table_name = process_csv_file(file_path)
                        else:
                            # Process CSV file directly
                            df, table_name = process_csv_file(uploaded_file)
                        
                        # Store in SQLite
                        result = store_dataframe_to_sqlite(df, table_name, SQLITE_DB_PATH)
                        st.success(f"CSV processed: {result}")
                
                st.success("All files processed successfully!")
                # Update session state to trigger UI refresh
                st.session_state.uploaded_files = uploaded_files

def query_tab():
    st.header("Query Your Data")
    
    # Query target selection
    query_target = st.radio(
        "Query Target",
        options=["Auto", "Document Store", "SQL Database"],
        horizontal=True,
        index=0,
    )
    
    st.session_state.query_target = query_target.lower()
    
    # Document selection for Document Store
    selected_doc = None
    if st.session_state.query_target == "document store":
        embedded_docs = list_embedded_documents()
        if embedded_docs:
            # Add "All Documents" option
            doc_options = ["All Documents"] + embedded_docs
            selected_doc = st.selectbox(
                "Select specific document to query (optional):",
                options=doc_options,
                index=0
            )
            
            if selected_doc == "All Documents":
                selected_doc = None
            
            st.session_state.selected_doc = selected_doc

    # Table selection for SQL Database
    selected_table = None
    if st.session_state.query_target == "sql database":
        sql_tables = get_all_tables(SQLITE_DB_PATH)
        if sql_tables:
            # Add "All Tables" option
            table_options = ["All Tables"] + sql_tables
            selected_table = st.selectbox(
                "Select specific table to query (optional):",
                options=table_options,
                index=0
            )
            
            if selected_table == "All Tables":
                selected_table = None
            
            st.session_state.selected_table = selected_table

    # Query input
    query = st.text_area("Enter your question:", height=100)
    
    if st.button("Submit Query", key="submit_query_main"):
        if not query:
            st.warning("Please enter a question.")
            return

        with st.spinner("Generating answer..."):
            # Auto mode - decide between SQL and Document Store
            if st.session_state.query_target == "auto":
                # Check if we have both SQL and document data
                has_sql = len(get_all_tables(SQLITE_DB_PATH)) > 0
                has_docs = len(list_embedded_documents()) > 0

                if has_sql and not has_docs:
                    st.session_state.query_target = "sql database"
                elif has_docs and not has_sql:
                    st.session_state.query_target = "document store"
                else:
                    # If we have both, try to determine best target
                    # For now, use simple keyword matching
                    sql_keywords = ["table", "database", "sql", "record", "column", "row"]
                    if any(keyword in query.lower() for keyword in sql_keywords):
                        st.session_state.query_target = "sql database"
                    else:
                        st.session_state.query_target = "document store"

            # Execute against the chosen target
            if st.session_state.query_target == "document store":
                # Use the selected document if specified
                answer, viz_file, has_viz = generate_answer_with_visualization(
                    query, 
                    selected_doc=st.session_state.selected_doc
                )

                st.subheader("Answer")
                st.markdown(answer)

                if has_viz and os.path.exists(viz_file):
                    st.subheader("Visualization")
                    try:
                        # Dynamically import the visualization file as a module
                        import importlib.util
                        spec = importlib.util.spec_from_file_location("visualization", viz_file)
                        visualization_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(visualization_module)
                    except Exception as e:
                        st.error(f"An error occurred while executing the visualization code: {e}")

            elif st.session_state.query_target == "sql database":
                # Use the selected table if specified
                response, success = execute_natural_language_query(
                    query, 
                    selected_table=st.session_state.selected_table
                )

                st.subheader("Answer")
                if success:
                    st.markdown(response["output"])

                    # Check if there's a dataframe in the response
                    if "intermediate_steps" in response:
                        for step in response["intermediate_steps"]:
                            if isinstance(step, tuple) and len(step) > 1:
                                action = step[0]
                                if hasattr(action, "args") and action.args.get("query", "").lower().startswith("select"):
                                    result = step[1]
                                    # Try to display as dataframe if possible
                                    try:
                                        if isinstance(result, str) and "row" in result.lower():
                                            # Try to extract query results
                                            st.subheader("Query Results")
                                            st.text(result)
                                        elif isinstance(result, pd.DataFrame):
                                            # Display the result as a DataFrame
                                            st.subheader("Query Results")
                                            st.dataframe(result)
                                    except Exception as e:
                                        st.error(f"Error displaying results: {e}")
                else:
                    st.error(response["error"])

def overview_tab():
    st.header("Data Overview")
    
    # SQL Database Overview
    st.subheader("SQL Database Tables")
    sql_tables = get_all_tables(SQLITE_DB_PATH)
    
    if sql_tables:
        for table in sql_tables:
            with st.expander(f"Table: {table}"):
                preview = get_table_preview(table)
                if "error" not in preview:
                    df = pd.DataFrame(preview["data"], columns=preview["columns"])
                    st.dataframe(df)
                else:
                    st.error(preview["error"])
    else:
        st.info("No SQL tables found. Upload CSV or Excel files to create tables.")
    
    # Document Store Overview
    st.subheader("Document Store")
    embedded_docs = list_embedded_documents()
    
    if embedded_docs:
        for doc in embedded_docs:
            st.write(f"- {doc}")
    else:
        st.info("No documents found in the vector store. Upload PDF files to add documents.")

# Display the active tab
if st.session_state.active_tab == "Upload":
    upload_tab()
elif st.session_state.active_tab == "Query":
    query_tab()
elif st.session_state.active_tab == "Overview":
    overview_tab()

def process_csv_file(uploaded_file, table_name=None):
    """Process a CSV file and return a pandas DataFrame."""
    # Check if uploaded_file is a file-like object or a file path
    if isinstance(uploaded_file, str):  # File path
        df = pd.read_csv(uploaded_file)
        file_name = os.path.basename(uploaded_file)
    else:  # File-like object
        df = pd.read_csv(uploaded_file)
        file_name = uploaded_file.name

    # Clean the table name
    return df, clean_table_name(table_name or os.path.splitext(file_name)[0])

def get_all_tables(db_path):
    """Get a list of all tables in the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    
    conn.close()
    return tables