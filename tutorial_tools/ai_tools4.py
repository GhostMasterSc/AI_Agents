import os
from colorama import Fore
import logfire
from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv
import sqlite3
from pydantic import BaseModel

load_dotenv()

# Configure logfire
logfire.configure()

# Define the model
model = OpenAIModel(model_name=os.getenv("LLM_MODEL_OPENAI"),
                    base_url=os.getenv("BASE_URL"),
                    api_key=os.getenv("OPENROUTER_API_KEY")
                    )
# Connect to the database         
# 
agent_db = Agent (model=model,system_prompt="You are an agent that can connect to a database and list the tables in it.")

class DatabaseConnection(BaseModel):
    name: str


@agent_db.tool
def connect_to_db(ctx: RunContext[str]) -> str:
    """Connect to the database"""
    conn = sqlite3.connect(ctx.deps.name)
    return conn


def list_tables(ctx: RunContext[DatabaseConnection]) -> str:
    """List all tables in the database"""

    conn = ctx.deps.conn
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Tables in the database:")
    for table in tables:
        print(f"- {table[0]}")
    
    conn.close()

# Example function to preview data from a specific table
def preview_table(table_name, limit=5):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Get data
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
    rows = cursor.fetchall()
    
    print(f"\nColumns in {table_name}:")
    print(columns)
    print(f"\nFirst {limit} rows of {table_name}:")
    for row in rows:
        print(row)
    
    conn.close()

