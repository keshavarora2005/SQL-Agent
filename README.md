# 🚀 LangChain SQL Agent (Chinook DB)

AI-powered SQL Agent built using **LangChain + Gemini + SQLite** that answers natural language questions from a database.

## 📌 Features
- Ask questions in plain English
- Agent automatically generates SQL
- Works with Chinook sample DB
- Powered by LangChain Agents

## 🛠 Tech Stack
- Python
- LangChain
- LangGraph
- Google Gemini
- SQLite

## 📂 Project Structure
sql-langchain-agent/
│── app.py
│── Chinook.db
│── requirements.txt
│── .env.example
│── notebooks/


## ⚙️ Setup

### 1 Install dependencies
pip install -r requirements.txt


### 2 Add API key
cp .env.example .env


Add your key inside `.env`

### 3 Run
python app.py


## 💡 Example Queries
- Show top 5 customers
- Total sales by country
- List all albums

## 👨‍💻 Author
Keshav Arora