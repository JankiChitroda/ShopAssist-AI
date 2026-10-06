import sqlite3

conn = sqlite3.connect("support_pilot.db")
cursor = conn.cursor()

# Fetch all rows from the dispatches table
cursor.execute("SELECT * FROM dispatches")
rows = cursor.fetchall()

print("--- DISPATCH RECORDS ---")
for row in rows:
    print(row)

conn.close()