from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import pandas as pd
import os
import re

load_dotenv()

def get_working_llm():
    """Get a working ChatGroq model with fallback options"""
    models_to_try = [
        "llama-3.1-8b-instant",  # Currently the only working model
        # Other models are decommissioned as of Sept 2025
    ]
    
    last_error = None
    for model in models_to_try:
        try:
            llm = ChatGroq(model=model, temperature=0)
            print(f"✅ Successfully initialized model: {model}")
            return llm
        except Exception as e:
            last_error = e
            error_msg = str(e).lower()
            if "model_decommissioned" in error_msg:
                print(f"❌ Model {model} decommissioned")
                continue
            elif "authentication" in error_msg or "api_key" in error_msg:
                print(f"❌ Authentication error for {model}: {str(e)}")
                # Don't continue if it's an auth error - all models will fail
                raise e
            else:
                print(f"⚠️ Error with {model}: {str(e)}")
                continue
    
    # If all models fail, raise the last error
    print(f"❌ All models failed. Last error: {last_error}")
    raise Exception(f"No working models available. Last error: {last_error}")

def get_sql_chain(db):
    """Create SQL generation chain"""
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
    
    # Get a working LLM with fallback models
    llm = get_working_llm()
    
    def get_schema(_):
        return db.get_table_info()
    
    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )

def get_response(user_query: str, db: SQLDatabase, chat_history: list):
    """Get AI response with SQL execution and natural language response"""
    sql_chain = get_sql_chain(db)
    
    # Get SQL query and execute it
    sql_query = sql_chain.invoke({
        "question": user_query,
        "chat_history": chat_history,
    })
    
    # Fix common SQL errors
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
    if sql_response:
        try:
            # Simple parsing for basic table data
            lines = str(sql_response).strip().split('\n')
            if len(lines) > 1:
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
                    if len(df.columns) <= 10:  # Only rename if reasonable number of columns
                        df.columns = [f'Column_{i+1}' for i in range(len(df.columns))]
        except:
            df = None
    
    # Apply automatic sampling for large datasets
    if df is not None and len(df) > 5000:
        df = df.sample(n=2000, random_state=42)
        sample_note = f"\n\n*Note: Showing sample of 2000 rows from {len(df)} total rows for performance.*"
    else:
        sample_note = ""
    
    if df is not None and (wants_table or len(df) > 0):
        response = f"Here is the result in tabular format:{sample_note}"
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
    
    Provide a clear, concise answer. Do not format data as ASCII tables - just describe the results naturally.{sample_note}"""
    
    prompt = ChatPromptTemplate.from_template(template)
    llm = get_working_llm()
    
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke({
        "question": user_query,
        "chat_history": chat_history,
        "schema": db.get_table_info(),
        "query": sql_query,
        "response": sql_response,
        "sample_note": sample_note
    })
    
    return response, df, sql_query
