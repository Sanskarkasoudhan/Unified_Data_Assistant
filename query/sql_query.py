from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import create_sql_agent
from config import GEMINI_API_KEY
from storage.sql_store import get_sql_database, execute_sql_query
import os

# Set up API key for Gemini model
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

def create_sql_agent_executor():
    """Create an SQL agent executor for natural language SQL queries."""
    # Initialize the Gemini LLM model
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.4)
    
    # Get SQL database connection
    db = get_sql_database()
    
    # Create an SQL agent
    agent_executor = create_sql_agent(
        llm,
        db=db,
        agent_type="openai-tools",
        verbose=True
    )
    
    return agent_executor

def execute_natural_language_query(query, selected_table=None):
    """
    Executes a natural language query against the SQL database.
    If a specific table is selected, limit the query to that table.
    """
    try:
        # Create the SQL agent executor
        agent_executor = create_sql_agent_executor()
        
        # If a specific table is selected, prepend it to the query as context
        if selected_table:
            query = f"Query the table '{selected_table}': {query}"
        
        # Use the agent to execute the query
        result = agent_executor.run(query)
        return {"output": result}, True
    except Exception as e:
        return {"error": str(e)}, False

# Example query
example_query = "show me all rows"
example_table = "table_name"
query = f"SELECT * FROM {example_table} WHERE {example_query}"