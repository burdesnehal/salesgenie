import streamlit as st
import mysql.connector
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.set_page_config(layout="wide")
st.title("🧠 SalesGenie: Smart SQL Chatbot")

# 🔄 UPDATED: Session initialization for chat and connection
if "connected" not in st.session_state:
    st.session_state.connected = False
if "conn" not in st.session_state:
    st.session_state.conn = None
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a senior MySQL expert chatbot helping users generate SQL queries and explain results from a sales database."}
    ]

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

def generate_sql_with_groq(messages):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.3,
        max_tokens=512
    )
    return response.choices[0].message.content.strip().strip("`")


# 🔄 UPDATED: Main chat input + response handling
st.subheader("🤖 Ask a question about your data")

question = st.chat_input("Ask your question here...")  # 🔄 UPDATED: chat-style input

if question and st.session_state.connected:
    try:
        # 🔄 UPDATED: add schema and question to chat history
        schema = get_schema(st.session_state.conn, database)
        st.session_state.messages.append({"role": "system", "content": f"The current database schema is:\n{schema}"})
        st.session_state.messages.append({"role": "user", "content": question})

        # 🔄 UPDATED: get SQL from LLM
        sql_query = generate_sql_with_groq(st.session_state.messages)

        # 🔄 UPDATED: run query and show result
        df = pd.read_sql(sql_query, st.session_state.conn)
        output_md = df.head().to_markdown(index=False)

        # 🔄 UPDATED: add assistant reply to chat
        assistant_msg = f"Here is the SQL query:\n```sql\n{sql_query}\n```\n\nAnd here are the results:\n\n{output_md}"
        st.session_state.messages.append({"role": "assistant", "content": assistant_msg})

    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"❌ Error: {e}"})

# 🔄 UPDATED: Display all chat messages like ChatGPT
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue  # don't display system message
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# Warning if not connected
if not st.session_state.connected:
    st.warning("Please connect to the MySQL database from the sidebar to begin.")