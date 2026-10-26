import sqlite3

db_path = 'C:/Users/augus/.gemini/antigravity/conversations/c8ce1688-5927-4b17-a8c5-9db55ccc2cb6.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("SELECT idx, step_type, status, typeof(metadata), typeof(step_payload) FROM steps ORDER BY idx ASC")
for row in cur.fetchall():
    print(row)

conn.close()
