

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import openai
import pandas as pd
import re
from schemas import accounts_income_schema, accounts_expense_schema
from urllib.parse import quote_plus
import pymysql
from pydantic import BaseModel
import json

# Load environment variables
load_dotenv()

class CalendarEvent(BaseModel):
    table_name: str
    is_aggregation: bool

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

def mysqlconnect():
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
    )
    return conn.cursor()

def detect_table_from_value(column, value):
    cursor = mysqlconnect()
    for table in ["accounts_income", "accounts_expense"]:
        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {column} = %s", (value,))
        if cursor.fetchone()[0] > 0:
            return table
    return None


def safe_is_select(sql: str) -> bool:
    return sql.strip().lower().startswith("select")

def execute_sql_return_df(sql: str):
    if not safe_is_select(sql):
        raise ValueError("Only SELECT queries are allowed.")
    
    cursor = mysqlconnect()
    cursor.execute(sql)
    output = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(output, columns=columns)
    return df

def ask_openai(prompt):
    """Helper function to call OpenAI ChatCompletion."""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

@app.route('/ask', methods=['POST'])

def ask():
    user_query = request.json['question']
    
    schemas_dict = {
        "accounts_income": accounts_income_schema,
        "accounts_expense": accounts_expense_schema
    }
    schemas_list = list(schemas_dict.keys())

   #Step 1: Schema selection
    topic_prompt = f"""

    The following are the tables in the MySQL database: accounts_income and accounts_expense.

    You are an expert MySQL query generator. Given a user question, choose the correct schema from the list above and provide the schema name.

    choose the correct row if user specifically asks data for income or expense.

    if the {user_query} requires both the tables return both 

    User question: {user_query}
    """

#     topic_prompt = f"""
# We have two tables:

# 1. accounts_income: Stores all incoming money transactions (revenue, receipts, sales, cash inflow).
# 2. accounts_expense: Stores all outgoing money transactions (purchases, bills to pay, cash outflow).

# When the user question mentions:
# - income, revenue, sales, receipts, or cash received → choose accounts_income
# - expense, cost, purchase, payment, bills paid, or cash spent → choose accounts_expense

# If both could apply, choose the one where the mentioned bill_name or keyword exists in the data.

# Return ONLY the exact table name: accounts_income or accounts_expense.

# User question: {user_query}
# """
    
    
    try:


        schema_text = ask_openai(topic_prompt)
        schema_text = re.sub(r'[`"\[\]]', '', schema_text)
        possible_names = [name for name in re.split(r'[,\s]+', schema_text) if name in schemas_list]
        if not possible_names:
            return jsonify({"error": f"Invalid schema name returned: {schema_text}"}), 400
        schema_name = possible_names[0]
        
        chart_type_prompt = f"Determine the chart type for the question. Give only one word: bar, line, or pie.\nQuestion: {user_query}"
        chart_type = ask_openai(chart_type_prompt)
        
        print(f"Schema name returned: {schema_name}, Chart type: {chart_type}")

    except Exception as e:
        return jsonify({"error": f"Schema selection error: {e}"}), 500

    if schema_name not in schemas_list:
        return jsonify({"error": f"Invalid schema name returned: {schema_name}"}), 400

    # Step 2: SQL generation
    schema_def = schemas_dict[schema_name]
    prompt = f"""
    table_name: {schema_name}
    Schema:
    {schema_def}

    Use the exact table and column names from the schema above. 
    i need structured output in JSON format.
    both
    I need 3 variables in the output:
    1. sql: the SQL query to answer the question
    2. is_aggregation: boolean indicating if the query is an aggregation query.
    3. datapoints_query: the SQL query to get the data points for the chart.
    Write ONLY a valid MySQL query (no explanation, no markdown formatting, no triple backticks) to answer this user question:
    Example:
    {{
        "sql": "SELECT ...",
        "is_aggregation": true,
        "datapoints_query": "SELECT label, value FROM ..."
    }}

    {user_query}
    """
    
    try:

        sql_json_str = ask_openai(prompt)
        sql_json = json.loads(sql_json_str)  # parse JSON
        # print(f"Generated SQL: {sql_query}")
    except Exception as e:
        return jsonify({"error": f"SQL generation error: {e}"}), 500
    
    sql_query = sql_json["sql"]
    is_aggregation = sql_json.get("is_aggregation", False)
    datapoints_query = sql_json.get("datapoints_query")

        # sql_query = ask_openai(prompt)
    print(f"Generated SQL: {sql_query}")
    # except Exception as e:
    #     return jsonify({"error": f"SQL generation error: {e}"}), 500

    # if sql_query.startswith("```sql"):
    #     sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    # Step 3: Execute SQL
    try:
        df = execute_sql_return_df(sql_query)
    except Exception as e:
        return jsonify({"error": f"SQL execution failed: {str(e)}", "sql": sql_query}), 500
    
    # Step 4: If aggregation → run datapoints query separately
    chart_data = []
    if is_aggregation and datapoints_query:
        try:
            df_chart = execute_sql_return_df(datapoints_query)
            chart_data = df_chart.to_dict(orient='records')
        except Exception as e:
            return jsonify({"error": f"Datapoints query failed: {str(e)}", "datapoints_query": datapoints_query}), 500

    # Step 4: Summary
    summary_prompt = f"Summarize this data in 1-2 sentences:\nData: {df.to_dict(orient='records')}\nUser question: {user_query}"
    summary = ask_openai(summary_prompt)

    # Step 5: Charts
    charts = []
    if is_aggregation and chart_data:
    # Use chart_data from aggregation for charts
        charts = [
        {
            'chartType': 'bar',
            'data': chart_data,
            'columns': list(chart_data[0].keys()) if chart_data else []
        },
        {
            'chartType': 'line',
            'data': chart_data,
            'columns': list(chart_data[0].keys()) if chart_data else []
        },
        {
            'chartType': 'pie',
            'data': chart_data,
            'columns': list(chart_data[0].keys()) if chart_data else []
        }
    ]
    # if is_aggregation and chart_data:
    # # Use chart_data from aggregation for charts
    #     charts = [
    #     {
    #         'chartType': chart_type,
    #         'data': chart_data,
    #         'columns': list(chart_data[0].keys()) if chart_data else []
    #     }
    # ]
    # else:
    # Non-aggregation charts use main df
    else:
        charts = [
        {
            'chartType': 'bar',
            'data': df.to_dict(orient='records'),
            'columns': list(df.columns)
        },
        {
            'chartType': 'line',
            'data': df.to_dict(orient='records'),
            'columns': list(df.columns)
        },
        {
            'chartType': 'pie',
            'data': df.to_dict(orient='records'),
            'columns': list(df.columns)
        }
    ]

    return jsonify({
        'sql': sql_query,
        'is_aggregation': is_aggregation,
        'datapoints_query': datapoints_query,
        'data': df.to_dict(orient='records'),
        'columns': list(df.columns),
        'summary': summary,
        'chartType': chart_type,
        'charts': charts,
        'chartData': chart_data  # separate aggregation chart points
    })

if __name__ == '__main__':
    app.run(debug=True)

