from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import streamlit as st
import pandas as pd
import os


def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
  db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
  return SQLDatabase.from_uri(db_uri)

def get_sql_chain(db):
  template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    
    <SCHEMA>{schema}</SCHEMA>
    
    IMPORTANT NOTES:
    - departments table has department_name column, use alias 'de' for departments
    - doctors table links to departments via department_id
    - prescriptions link directly to patients and doctors (no appointment_id needed)
    - Always use de.department_name (not d.department_name) when referencing department names
    
    MySQL GROUP BY RULES (CRITICAL - NEVER VIOLATE):
    - When using GROUP BY, ALL non-aggregate columns in SELECT must be in GROUP BY clause
    - NEVER select p.first_name, p.last_name with GROUP BY de.department_name
    - If grouping by department: ONLY select de.department_name and aggregate functions
    - If showing individual patients: GROUP BY p.patient_id, NOT by department
    
    CORRECT PATTERNS:
    - Count by department: SELECT de.department_name, COUNT(*) as patient_count FROM ... GROUP BY de.department_name
    - List patients in department: SELECT p.first_name, p.last_name, de.department_name FROM ... (NO GROUP BY)
    - Patients with details: SELECT p.first_name, p.last_name, GROUP_CONCAT(de.department_name) FROM ... GROUP BY p.patient_id
    
    FORBIDDEN PATTERNS:
    - ❌ SELECT p.first_name, p.last_name, de.department_name FROM ... GROUP BY de.department_name
    - ❌ Any individual column with GROUP BY on different column
    
    Conversation History: {chat_history}
    
    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
    For example:
    Question: Show patients with prescriptions from multiple departments
    SQL Query: SELECT p.first_name, p.last_name, GROUP_CONCAT(DISTINCT de.department_name) AS departments FROM patients p JOIN prescriptions pr ON p.patient_id = pr.patient_id JOIN doctors d ON pr.doctor_id = d.doctor_id JOIN departments de ON d.department_id = de.department_id GROUP BY p.patient_id HAVING COUNT(DISTINCT de.department_id) > 1;
    
    Your turn:
    
    Question: {question}
    SQL Query:
    """
    
  prompt = ChatPromptTemplate.from_template(template)
  
  # llm = ChatOpenAI(model="gpt-4-0125-preview")
  llm = ChatGroq(model="llama3-70b-8192", temperature=0, api_key=os.getenv("GROQ_API_KEY"))
  
  def get_schema(_):
    return db.get_table_info()
  
  return (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | llm
    | StrOutputParser()
  )
    
def get_response(user_query: str, db: SQLDatabase, chat_history: list):
  sql_chain = get_sql_chain(db)
  
  # Get SQL query and execute it
  sql_query = sql_chain.invoke({
    "question": user_query,
    "chat_history": chat_history,
  })
  
  # Fix common SQL errors
  import re
  sql_query = re.sub(r'\bd\.department_name\b', 'de.department_name', sql_query)
  sql_query = re.sub(r'GROUP_CONCAT\(DISTINCT d\.department_name', 'GROUP_CONCAT(DISTINCT de.department_name', sql_query)
  
  try:
    sql_response = db.run(sql_query)
  except Exception as e:
    # Try to fix the query if it has department_name error
    if 'd.department_name' in str(e):
      fixed_query = re.sub(r'\bd\.department_name\b', 'de.department_name', sql_query)
      try:
        sql_response = db.run(fixed_query)
        sql_query = fixed_query
      except:
        return f"Error executing query: {str(e)}", None, None
    else:
      return f"Error executing query: {str(e)}", None, None
  
  # Check if user wants tabular format
  wants_table = 'tabular' in user_query.lower() or 'table' in user_query.lower()
  
  # Try to parse SQL response as DataFrame
  df = None
  if wants_table and sql_response:
    try:
      # Simple parsing for basic table data
      lines = str(sql_response).strip().split('\n')
      if len(lines) > 1:
        import pandas as pd
        # Parse simple tuple format like "(1, 'John', 'Smith')"
        data = []
        for line in lines:
          if line.strip().startswith('(') and line.strip().endswith(')'):
            # Remove parentheses and split by comma
            values = line.strip()[1:-1].split(', ')
            # Clean up quotes
            values = [v.strip("'\"") for v in values]
            data.append(values)
        
        if data:
          # Create DataFrame with generic column names
          df = pd.DataFrame(data)
          if len(df.columns) <= 3:
            df.columns = [f'Column_{i+1}' for i in range(len(df.columns))]
    except:
      df = None
  
  if df is not None and wants_table:
    response = "Here is the result in tabular format:"
    return response, df, sql_query
  
  # Generate natural language response
  template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}
    
    Provide a clear, concise answer. Do not format data as ASCII tables - just describe the results naturally."""
  
  prompt = ChatPromptTemplate.from_template(template)
  llm = ChatGroq(model="llama3-8b-8192", temperature=0, api_key=os.getenv("GROQ_API_KEY"))
  
  chain = prompt | llm | StrOutputParser()
  
  response = chain.invoke({
    "question": user_query,
    "chat_history": chat_history,
    "schema": db.get_table_info(),
    "query": sql_query,
    "response": sql_response,
  })
  
  return response, df, sql_query
    
  
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
      AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database."),
    ]

load_dotenv()

st.set_page_config(page_title="Chat with MySQL", page_icon=":speech_balloon:")

st.title("DrQuery")

with st.sidebar:
    st.subheader("Settings")
    
    st.text_input("Host", value="localhost", key="Host")
    st.text_input("Port", value="3306", key="Port")
    st.text_input("User", value="root", key="User")
    st.text_input("Password", type="password", value="admin", key="Password")
    st.text_input("Database", value="drqueryDB", key="Database")
    
    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            db = init_database(
                st.session_state["User"],
                st.session_state["Password"],
                st.session_state["Host"],
                st.session_state["Port"],
                st.session_state["Database"]
            )
            st.session_state.db = db
            st.success("Connected to database!")
    
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

user_query = st.chat_input("Type a message...")
if user_query is not None and user_query.strip() != "":
    if "db" not in st.session_state:
        st.error("Please connect to the database first using the sidebar.")
    else:
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        
        with st.chat_message("Human"):
            st.markdown(user_query)
            
        with st.chat_message("AI"):
            response, df, sql_query = get_response(user_query, st.session_state.db, st.session_state.chat_history)
            
            # Display response and table together
            if df is not None:
                # Remove extra spacing by combining text and table
                st.markdown(response)
                st.dataframe(df, use_container_width=True)
            else:
                st.markdown(response)
            
            # Show SQL query in expander if requested
            if sql_query and ('sql' in user_query.lower() or 'query' in user_query.lower()):
                with st.expander("🔍 View SQL Query"):
                    st.code(sql_query, language="sql")
            
        st.session_state.chat_history.append(AIMessage(content=response))