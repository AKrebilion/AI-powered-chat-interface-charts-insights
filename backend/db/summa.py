import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("northwind.db")
cursor = conn.cursor()

# Fetch all table names
cursor.execute("SELECT CategoryName, COUNT(ProductID) as ProductCount FROM Products GROUP BY CategoryName LIMIT 5;")
tables = cursor.fetchall()

print("Tables in DB:")
for table in tables:
    table_name = table[0]
    print(f"\n--- Schema of '{table_name}' ---")
    
    # Fetch schema info
    cursor.execute(f"PRAGMA table_info('{table_name}');")
    schema = cursor.fetchall()
    
    for column in schema:
        print(column)

# Close connection
conn.close()
