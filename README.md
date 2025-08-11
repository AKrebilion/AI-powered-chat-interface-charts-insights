# AI-Powered Chat Interface with Charts and Insights

## Overview

This project is an AI-powered chat interface that enables users to interact with data using natural language queries. It generates SQL queries on-the-fly and visualizes the results using dynamic charts and insightful summaries.

The backend is built with Flask and integrates with OpenAI APIs to process queries and generate SQL commands against the Northwind SQLite database. The frontend is a React application that provides a smooth chat experience along with data visualization using charts.

---

## Features

- Natural language querying of the Northwind database
- AI-generated SQL queries powered by OpenAI
- Dynamic chart visualizations (bar, line, pie charts)
- Insightful summaries based on query results
- Full-stack integration with Flask backend and React frontend

---

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Git

### Backend Setup

1. Navigate to the backend folder:
   ```bash
   cd backend

2.Create a virtual environment and activate it:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate


3.Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt


4.Set your OpenAI API key in a .env file:

ini
Copy
Edit
OPENAI_API_KEY=your_api_key_here


5.Run the Flask server:

bash
Copy
Edit
flask run




#Frontend Setup
1.Navigate to the frontend folder:
bash
Copy
Edit
cd frontend

2.Install dependencies:
bash
Copy
Edit
npm install

3.Start the React development server:
bash
Copy
Edit
npm start

#Usage
Open the React app in your browser (usually at http://localhost:3000).

Type natural language queries in the chat interface.

View dynamic charts and summaries generated based on your queries.

#Technologies Used
Python, Flask

React.js

OpenAI API (GPT / Gemini)

SQLite (Northwind database)

Chart.js or similar charting libraries
