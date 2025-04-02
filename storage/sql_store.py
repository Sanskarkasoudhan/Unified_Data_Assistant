import sqlite3
from langchain_community.utilities import SQLDatabase
from config import SQLITE_DB_PATH

def get_sql_database():
    """Get a SQLDatabase instance for the SQLite database."""
    return SQLDatabase.from_uri(f"sqlite:///{SQLITE_DB_PATH}")

def execute_sql_query(query):
    """Execute an SQL query directly and return the results."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description] if cursor.description else []
        
        conn.close()
        return {"columns": column_names, "data": results}
    
    except Exception as e:
        conn.close()
        raise e

def get_table_preview(table_name, limit=5):
    """Get a preview of data in a table."""
    try:
        result = execute_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}")
        return result
    except Exception as e:
        return {"error": str(e)}

def get_database_info():
    """Get information about all tables in the database."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Get schema and row count for each table
    database_info = []
    for table in tables:
        table_name = table[0]
        
        # Get column info
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cursor.fetchone()[0]
        
        database_info.append({
            "name": table_name,
            "columns": columns,
            "row_count": row_count
        })
    
    conn.close()
    return database_info

def infer_table_relationships(db_path):
    """Infer relationships between tables in the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    
    relationships = []
    
    for table in tables:
        # Get columns for the current table
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        # Check for potential foreign key relationships
        for other_table in tables:
            if table == other_table:
                continue
            
            cursor.execute(f"PRAGMA table_info({other_table});")
            other_columns = cursor.fetchall()
            other_column_names = [col[1] for col in other_columns]
            
            # Infer relationships based on column names
            for col in column_names:
                if col in other_column_names:
                    relationships.append({
                        "from_table": table,
                        "from_column": col,
                        "to_table": other_table,
                        "to_column": col
                    })
    
    conn.close()
    return relationships