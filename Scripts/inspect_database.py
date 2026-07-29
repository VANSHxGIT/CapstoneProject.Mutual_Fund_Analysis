import sqlite3
from config import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]

for table in tables:
    print(f"\n===== {table} =====")
    cursor.execute(f"PRAGMA table_info('{table}')")
    for column in cursor.fetchall():
        print(column)

conn.close()