🧠 SalesGenie: Smart SQL Chatbot

SalesGenie is an intelligent chatbot interface that transforms natural language queries into SQL, connects to MySQL databases, and visualizes results with interactive charts. It supports user authentication, generates smart queries using LLMs (Groq's LLaMA3 via OpenAI-compatible API), and displays rich analytical insights.

📌 Features
🔐 User Login/Signup system with password hashing

🧠 AI-generated SQL using LLaMA3 via Groq API

📊 Instant data visualization (bar, pie, scatter, histogram, etc.)

💬 Chat-like interface for querying any MySQL database

🛠️ Dynamic schema detection and sample question generation

📦 Session and chat log management

🧩 Modular design with clean code separation

📋 Tech Stack
Layer	Technology
Frontend	Streamlit
Backend/API	Python (OpenAI-compatible SDK)
Authentication	bcrypt, custom logic
LLM Integration	Groq API (LLaMA3-70B-8192)
DB Connection	MySQL + mysql.connector
Visualization	Plotly, Pandas
Env Management	Python-dotenv
Session Mgmt	Streamlit session_state

🚀 Installation
📦 Prerequisites
Python 3.8+
MySQL database
Groq/OpenAI API key
.env file (create in root)

📁 Clone the Repo

git clone https://github.com/yourusername/SalesGenie.git
cd SalesGenie

🧪 Install Dependencies
pip install -r requirements.txt

🔐 Setup Environment Variables
Create a .env file:
GROQ_API_KEY=your_groq_api_key
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=yourpassword
DB_NAME=salesgenie

🎮 Usage
Run the chatbot with Streamlit:
streamlit run app.py

💡 Sample Interaction
🔐 Login or Sign Up
User logs in or signs up via the SalesGenie web app interface.
👤 Login Page

Users can securely log in using their username or email and password.

🔒 Passwords are masked with the ability to toggle visibility.

❌ If login credentials are invalid, users receive immediate error feedback.

<img width="1917" height="858" alt="Screenshot 2025-07-13 150600" src="https://github.com/user-attachments/assets/203655e2-9833-47d4-995b-c98d88fc83e8" />


📝 Sign Up Page

New users can create an account with:

Unique username

Email

Password (with confirmation)

📏 Passwords must be at least 8 characters long.

✅ Secure password hashing is handled via bcrypt.

<img width="1919" height="845" alt="Screenshot 2025-07-13 151542" src="https://github.com/user-attachments/assets/e1b670d5-e378-49c9-8529-1efd4a5093f6" />



🔗 Connect to Your MySQL Database
Prompted Fields:

Host: localhost

Port: 3306

Username: your_username

Password: your_password

Database: salesgenie

✅ Connection Established Successfully
<img width="1919" height="854" alt="Screenshot 2025-07-13 150829" src="https://github.com/user-attachments/assets/08889ec6-92c7-40e9-baaf-acf5d898582b" />


🧠 SalesGenie AI Features
Reads the Database Schema

Tables Detected: users, chat_logs, sales_data, products, orders, etc.

Generates 5 Smart Questions (Example):

What are the total sales by product category in the last quarter?

Who are the top 5 customers by revenue?

Which region had the highest sales last month?

What is the monthly trend of total sales this year?

What are the top-selling products in the last 30 days?

🤖 User Asks in Natural Language:
"What are the total sales by product category in the last quarter?"
<img width="1919" height="848" alt="Screenshot 2025-07-13 151105" src="https://github.com/user-attachments/assets/1fd26042-0c85-4ac1-88be-e2fc54efd2be" />


🧬 SalesGenie AI Flow:
Parses Natural Language Input using LLaMA3 via Groq API

Generates SQL:
SELECT product_category, SUM(total_sales) AS total_sales
FROM sales_data
WHERE sale_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
GROUP BY product_category;
Executes Query on Connected MySQL DB

📊 Displays Results
Tabular View:
Product Category	Total Sales
Electronics	₹1,25,000
Apparel	₹85,000
Home Appliances	₹95,500

Graphical View (Bar Chart):
🟦 Electronics
🟩 Apparel
🟨 Home Appliances
(Bar heights represent total sales)
<img width="1919" height="849" alt="Screenshot 2025-07-13 151448" src="https://github.com/user-attachments/assets/32b407fd-bf6a-4d01-b4b4-626d7cf87a73" />
<img width="1919" height="856" alt="Screenshot 2025-07-13 151502" src="https://github.com/user-attachments/assets/bcf207fa-f7f4-4609-81df-ed5261aaa16e" />



✅ Query Complete! Ask More Questions or Export Results.

