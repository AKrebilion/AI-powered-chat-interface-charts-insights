# 🤖 AI-Powered Chat Interface with Charts and Insights 📊

## 🔍 Overview

This project is an AI-powered chat interface that lets users interact with data using natural language queries. It generates SQL queries on-the-fly and visualizes the results with dynamic charts and insightful summaries.

The backend is built with **Flask** and integrates with **OpenAI APIs** to process queries and generate SQL commands against the **Northwind SQLite database**. The frontend is a **React** app providing a smooth chat experience alongside rich data visualizations..

---

## ✨ Features

- 🗣️ Natural language querying of the Northwind database  
- 🤖 AI-generated SQL queries powered by OpenAI  
- 📈 Dynamic chart visualizations (bar, line, pie charts)  
- 💡 Insightful summaries based on query results  
- 🔄 Full-stack integration with Flask backend and React frontend  

---

## 🚀 Getting Started

### 🛠️ Prerequisites

- Python 3.8+  
- Node.js 14+  
- Git  

---

### 🐍 Backend Setup

1. **Navigate to backend folder:** 
   ```bash
   cd backend

# 2. **Create a virtual environment:**
python -m venv venv

 3.Activate the virtual environment:
 
# On Linux/macOS:
source venv/bin/activate
# On Windows Command Prompt:
venv\Scripts\activate
# On Windows PowerShell:
# .\venv\Scripts\Activate.ps1

# 4. Install backend dependencies:
pip install -r requirements.txt

# 5. Create a .env file with your OpenAI API key:
echo OPENAI_API_KEY=your_api_key_here > .env

# 6. Run the Flask backend server:
flask run

# =======

# In a new terminal window/tab:

# 7. Navigate to frontend folder:
cd frontend

# 8. Install frontend dependencies:
npm install

# 9. Start the React development server:
npm start
