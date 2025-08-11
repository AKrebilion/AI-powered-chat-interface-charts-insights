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

### Backend Setup

1. Navigate to the backend folder:  
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:  
   ```bash
   python -m venv venv
   # On Linux/macOS:
   source venv/bin/activate
   # On Windows (Command Prompt):
   venv\Scripts\activate
   ```

3. Install backend dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend folder and add your OpenAI API key:  
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. Run the Flask backend server:  
   ```bash
   flask run
   ```

### Frontend Setup

1. Open a new terminal window/tab.

2. Navigate to the frontend folder:  
   ```bash
   cd frontend
   ```

3. Install frontend dependencies:  
   ```bash
   npm install
   ```

4. Start the React development server:  
   ```bash
   npm start
   ```

## Usage

- Open your browser and go to:  
  `http://localhost:3000`  

- Use the chat interface to type natural language queries.  
- View dynamic charts and summaries generated from your queries.

## Technologies Used

- Python & Flask  
- React.js  
- OpenAI API  
- SQLite (Northwind database)  
- Chart.js (or similar charting libraries)  

# 9. Start the React development server:
npm start
