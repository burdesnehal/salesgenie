import streamlit as st
import mysql.connector
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
from openai import OpenAI
import os


# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(layout="wide")
st.title("🧠 SalesGenie: Smart SQL Chatbot")

# Session init
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'conn' not in st.session_state:
    st.session_state.conn = None

# Sidebar - Database credentials form
st.sidebar.markdown("### 🗃️ Connect to MySQL Database")
with st.sidebar.form("db_form"):
    host = st.text_input("Host", "localhost")
    port = st.text_input("Port", "3306")
    database = st.text_input("Database")
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("🔌 Connect")

if submitted:
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        st.session_state.conn = conn
        st.session_state.connected = True
        st.sidebar.success("✅ Connected successfully")
    except Exception as e:
        st.session_state.connected = False
        st.sidebar.error(f"❌ Failed: {e}")

# Sidebar - Reference questions (bottom part)
st.sidebar.markdown("### 💡 Sample Questions")
sample_questions = [
    "What are total sales by year?",
    "List top 5 products by quantity sold",
    "Who are top 3 customers by revenue?",
    "Show monthly revenue for 2024",
    "What regions have highest orders?"
]
for q in sample_questions:
    st.sidebar.markdown(f"- {q}")

# Function to get DB schema
def get_schema(conn, db):
    cursor = conn.cursor()
    cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{db}'")
    tables = cursor.fetchall()

    schema = ""
    for (table,) in tables:
        cursor.execute(f"DESCRIBE {table}")
        columns = cursor.fetchall()
        schema += f"\nTable `{table}`:\n"
        for col in columns:
            schema += f"- {col[0]} ({col[1]})\n"
    return schema


client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_sql_with_groq(question, schema):
    prompt = f"""
You are a senior MySQL expert. Given the following database schema:

{schema}

Generate a syntactically correct and optimized SQL query to answer the question:
"{question}"

Only return the SQL code. Do not explain.
"""
    response = client.chat.completions.create(
    
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=512
    
    )
    return response.choices[0].message.content.strip().strip("`")

# Main UI (Right Panel)
st.subheader("🤖 Ask a question about your data")


if st.session_state.connected:
    question = st.text_input("Ask your question in plain English")
    if st.button("🚀 Generate & Run Query"):
        try:
            schema = get_schema(st.session_state.conn, database)
            sql_query = generate_sql_with_groq(question, schema)
            df = pd.read_sql(sql_query, st.session_state.conn)
            st.dataframe(df)
        except Exception as e:
            st.error(f"❌ Query failed: {e}")
else:
    st.warning("Connect to the database from the sidebar to start.")
    