# 🧠 SalesGenie: Smart SQL Chatbot

SalesGenie is an intelligent chatbot interface that transforms natural language queries into SQL, connects to MySQL databases, and visualizes results with interactive charts. It supports user authentication, generates smart queries using LLMs (Groq's LLaMA3 via OpenAI-compatible API), and displays rich analytical insights.

---

## 📌 Features

- 🔐 User Login/Signup system with secure password hashing
- 🧠 AI-generated SQL using LLaMA3 via Groq API
- 📊 Instant data visualization (bar, pie, scatter, histogram, etc.)
- 💬 Chat-like interface for querying any MySQL database
- 🛠️ Dynamic schema detection and smart question suggestions
- 📦 Session and chat log management
- 🧩 Modular design with clean code separation

---

## 📋 Tech Stack

| Layer           | Technology                         |
|----------------|-------------------------------------|
| Frontend       | Streamlit                          |
| Backend/API    | Python (OpenAI-compatible SDK)     |
| Authentication | bcrypt, custom logic               |
| LLM Integration| Groq API (LLaMA3-70B-8192)         |
| DB Connection  | MySQL + mysql.connector            |
| Visualization  | Plotly, Pandas                     |
| Env Management | python-dotenv                      |
| Session Mgmt   | Streamlit `session_state`          |

---

## 🚀 Installation

### 📦 Prerequisites
- Python 3.8+
- MySQL database
- Groq/OpenAI API key
- `.env` file in root directory

### 📁 Clone the Repo

```bash
git clone https://github.com/yourusername/SalesGenie.git
cd SalesGenie
