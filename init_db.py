# init_db.py
import sqlite3
from pathlib import Path

db_path = Path("instance/contact_messages.db")
db_path.parent.mkdir(exist_ok=True)
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()
conn.close()
print("Database initialized at", db_path)
