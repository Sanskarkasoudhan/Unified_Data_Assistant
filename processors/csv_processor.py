import pandas as pd
import sqlite3
import os

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

def process_excel_file(uploaded_file, table_name=None):
    """Process an Excel file and return a pandas DataFrame."""
    # Read Excel into DataFrame
    df = pd.read_excel(uploaded_file)
    return df, clean_table_name(table_name or os.path.splitext(uploaded_file.name)[0])

def clean_table_name(name):
    """Clean table name to be SQL-friendly."""
    # Remove spaces, special characters and make lowercase
    cleaned_name = ''.join(c if c.isalnum() else '_' for c in name)
    # Ensure it doesn't start with a number
    if cleaned_name[0].isdigit():
        cleaned_name = 'table_' + cleaned_name
    return cleaned_name.lower()

def store_dataframe_to_sqlite(df, table_name, db_path):
    """Store a DataFrame to SQLite database."""
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    
    # Convert DataFrame to SQL table
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    return f"✅ Data stored in table '{table_name}'"

def get_table_schema(db_path, table_name):
    """Get the schema of a table."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
        
    # Get schema information
    cursor.execute(f"PRAGMA table_info({table_name});")
    schema = cursor.fetchall()
    
    conn.close()
    return schema

def get_all_tables(db_path):
    """Get a list of all tables in the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    
    conn.close()
    return tables