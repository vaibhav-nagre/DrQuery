from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os

load_dotenv()

def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
    """Initialize database connection"""
    db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)

def get_sql_chain(db):
    """Create SQL generation chain"""
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    
    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
    For example:
    Question: which 3 artists have the most tracks?
    SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
    Question: Name 10 artists
    SQL Query: SELECT Name FROM Artist LIMIT 10;
    
    Your turn:
    
    Question: {question}
    SQL Query:
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Use Groq for faster responses
    llm = ChatGroq(model="llama3-8b-8192", temperature=0, api_key=os.getenv("GROQ_API_KEY"))
    
    def get_schema(_):
        return db.get_table_info()
    
    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )

def get_response(user_query: str, db: SQLDatabase, chat_history: list):
    """Generate response to user query"""
    sql_chain = get_sql_chain(db)
    
    # Get the SQL query first
    sql_query = sql_chain.invoke({
        "question": user_query,
        "chat_history": chat_history,
    })
    
    # Execute the query
    try:
        sql_response = db.run(sql_query)
    except Exception as e:
        return f"Error executing query: {str(e)}"
    
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    
    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}
    
    Provide a clear, concise answer that explains the results in business terms. If there are interesting insights, highlight them.
    Only include the SQL query in a code block if the user specifically asks for the query, SQL, or how the data was retrieved.
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    llm = ChatGroq(model="llama3-8b-8192", temperature=0, api_key=os.getenv("GROQ_API_KEY"))
    
    chain = prompt | llm | StrOutputParser()
    
    return chain.invoke({
        "question": user_query,
        "chat_history": chat_history,
        "schema": db.get_table_info(),
        "query": sql_query,
        "response": sql_response,
    })