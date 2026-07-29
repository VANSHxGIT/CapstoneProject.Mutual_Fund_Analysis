import sqlite3

from config import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)

cursor = conn.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)

tables = cursor.fetchall()

for table in tables:

    table_name = table[0]

    print("\n" + "=" * 50)
    print(table_name)
    print("=" * 50)

    cursor.execute(
        f"PRAGMA table_info('{table_name}')"
    )

    columns = cursor.fetchall()

    for column in columns:
        print(column)

conn.close()