import streamlit as st
import mysql.connector
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
from openai import OpenAI
import os
import plotly.express as px
from auth import authenticate, create_user  
import db 

from dotenv import load_dotenv
load_dotenv(override=True)
print("🔑 Loaded key:", os.getenv("GROQ_API_KEY"))


# ------------------ Session State Initialization ------------------
if "auth" not in st.session_state:
    st.session_state.auth = {"is_auth": False, "user": None}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "connected" not in st.session_state:
    st.session_state.connected = False
if "conn" not in st.session_state:
    st.session_state.conn = None
if "sample_questions" not in st.session_state:
    st.session_state.sample_questions = []
if "auth" not in st.session_state:          
    st.session_state.auth = {               
        "is_auth": False,                   
        "user": None                        
    }           

st.set_page_config(layout="wide")
st.title(" SalesGenie: Smart SQL Chatbot")

# ------------------ LLM Client ------------------

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# ------------------ Functions ------------------

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

def generate_sample_questions(schema_text):
    prompt = f"""
You are an AI assistant. Based on the following MySQL database schema:

{schema_text}

Generate 5 helpful analytical or business questions a user might ask about this database. 
Return only the questions as a bullet list in plain English.
"""
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=512
    )
    
    output = response.choices[0].message.content.strip()
    lines = [line.strip() for line in output.split("\n") if line.strip()]


    questions = []
    for line in lines:
        clean = line.lstrip("-•1234567890. ").strip()
        if not clean.lower().startswith("here are"):
            questions.append(clean)

    return questions

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

# ------------------ Sidebar: DB Connection ------------------

# ------------------ Sidebar: DB Connection + Sample Questions ------------------

with st.sidebar:
    # ---------- ACCOUNT ----------
    st.markdown("## 🔑 Account")

    if not st.session_state.auth["is_auth"]:
        tabs = st.tabs(["Log In", "Sign Up"])

        # --- Log In ---
        with tabs[0]:
            usr = st.text_input("Username or Email", key="login_usr")
            pwd = st.text_input("Password", type="password", key="login_pwd")
            if st.button("Login"):
                user = authenticate(usr, pwd)
                if user:
                    st.session_state.auth = {"is_auth": True, "user": user}
                    st.success(f"Welcome {user['username']}! 👋")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

        # --- Sign Up ---
        with tabs[1]:
            new_usr  = st.text_input("Username", key="su_usr")
            new_mail = st.text_input("Email", key="su_email")
            new_pw1  = st.text_input("Password", type="password", key="su_pw1")
            new_pw2  = st.text_input("Confirm Password", type="password", key="su_pw2")
            if st.button("Create Account"):
                if new_pw1 != new_pw2:
                    st.warning("Passwords don't match.")
                elif len(new_pw1) < 8:
                    st.warning("Use at least 8 characters.")
                else:
                    ok, msg = create_user(new_usr, new_mail, new_pw1)
                    if ok:  st.success(msg)
                    else:   st.error(msg)
    else:
        user = st.session_state.auth["user"]
        st.success(f"Logged in as **{user['username']}**")
        if st.button("Log Out"):
            st.session_state.auth = {"is_auth": False, "user": None}
            st.rerun()


    # ---------- DB CONNECTION (only if logged in) ----------
    if st.session_state.auth["is_auth"]:
        st.markdown("### Connect to MySQL Database")
        with st.form("db_form"):
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
                st.success(" Connected successfully")

                #  Generate schema + smart questions
                schema = get_schema(conn, database)
                st.session_state.schema = schema
                st.session_state.sample_questions = generate_sample_questions(schema)

            except Exception as e:
                st.session_state.connected = False
                st.error(f" Failed: {e}")

        if st.session_state.connected and st.session_state.sample_questions:
            st.markdown("###  Sample Questions")
            for i, q in enumerate(st.session_state.sample_questions):
                if st.button(q, key=f"sample_{i}"):
                    st.session_state["new_question"] = q
        else:
            st.info("Connect to a database to generate smart sample questions.")

# ---------- SECURITY GATE ----------
if not st.session_state.auth["is_auth"]:
    st.warning("Please log in to access SalesGenie ")
    st.stop()


# Main UI (Right Panel)
# 1️ Floating Chat Input CSS
st.markdown("""
    <style>
        .floating-input {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 10px 20px;
            box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.1);
            z-index: 9999;
        }
        .floating-input input {
            width: 70% !important;
        }
        .floating-input .stButton {
            margin-left: 10px;
        }
        .block-container {
            padding-bottom: 100px; /* prevent content being hidden */
        }
    </style>
""", unsafe_allow_html=True)

# 2 Clear input before rendering
if st.session_state.get("clear_input"):
    st.session_state["new_question"] = ""
    st.session_state["clear_input"] = False

# 3️ Title & Chat History
st.subheader("Chat with your data!")

if st.session_state.connected:
    for i, chat in enumerate(st.session_state.chat_history):
        st.markdown(f"**🧑 You:** {chat['question']}")
       

        if 'result' in chat:
            df = chat['result']
            st.dataframe(df, use_container_width=True)

            #  Visualization
            #  Enhanced Visualization
            with st.expander(" Visualize this output"):
                if not df.empty:
                    col1, col2 = st.columns(2)
                    x_axis = col1.selectbox("Select X-axis", df.columns, key=f"x_{i}")
                    y_axis = col2.selectbox("Select Y-axis", df.columns, key=f"y_{i}")
                    chart_type = st.selectbox(
                        "Chart Type",
                        ["Line", "Bar", "Area", "Pie", "Scatter", "Histogram", "Box"],
                        key=f"chart_{i}"
                    )

                    if st.button("🖼 Show Chart", key=f"chart_btn_{i}"):
                        try:
                            if chart_type == "Line":
                                st.line_chart(df.set_index(x_axis)[y_axis])
                            elif chart_type == "Bar":
                                st.bar_chart(df.set_index(x_axis)[y_axis])
                            elif chart_type == "Area":
                                st.area_chart(df.set_index(x_axis)[y_axis])
                            elif chart_type == "Pie":
                                pie_df = df.groupby(x_axis)[y_axis].sum().reset_index()
                                st.plotly_chart(
                                    px.pie(pie_df, values=y_axis, names=x_axis, title="Pie Chart"),
                                    use_container_width=True
                                )
                            elif chart_type == "Scatter":
                                st.plotly_chart(
                                    px.scatter(df, x=x_axis, y=y_axis, title="Scatter Plot"),
                                    use_container_width=True
                                )
                            elif chart_type == "Histogram":
                                st.plotly_chart(
                                    px.histogram(df, x=y_axis, title="Histogram"),
                                    use_container_width=True
                                )
                            elif chart_type == "Box":
                                st.plotly_chart(
                                    px.box(df, x=x_axis, y=y_axis, title="Box Plot"),
                                    use_container_width=True
                                )
                        except Exception as e:
                            st.error(f"Chart Error: {e}")


# 4️ Floating Input Section
with st.container():
    st.markdown('<div class="floating-input">', unsafe_allow_html=True)

    with st.form(key="query_form", clear_on_submit=False):
        question = st.text_input("Ask your question...", key="new_question", label_visibility="collapsed")
        submitted = st.form_submit_button(" Generate & Run Query")
        if submitted:
            if question.strip() != "":
                try:
                    schema = get_schema(st.session_state.conn, database)
                    sql_query = generate_sql_with_groq(question, schema)
                    df = pd.read_sql(sql_query, st.session_state.conn)

                    st.session_state.chat_history.append({
                        "question": question,
                        "sql": sql_query,
                        "result": df
                    })
                    if st.session_state.auth["is_auth"] and st.session_state.auth["user"]:
                        user_id = st.session_state.auth["user"]["id"]
                        db.run(
                            "INSERT INTO chat_logs (user_id, question, sql_code) VALUES (%s, %s, %s)",
                            (user_id, question, sql_query)
                        )

                    st.session_state.clear_input = True
                    st.rerun()


                except Exception as e:
                    st.error(f" Query failed: {e}")
            else:
                st.warning(" Please enter a question.")

    st.markdown('</div>', unsafe_allow_html=True)

