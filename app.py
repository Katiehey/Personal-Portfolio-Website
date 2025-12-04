# app.py
from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__, static_folder="static", template_folder="templates")
DB_PATH = Path("instance/contact_messages.db")

def get_db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"status": "error", "message": "All fields are required."}), 400

    conn = get_db_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
        (name, email, message),
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Thanks — message received!"})

@app.route("/messages", methods=["GET"])
def list_messages():
    # simple endpoint to view messages (not authenticated). You can remove or protect this later.
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("SELECT id, name, email, message, created_at FROM messages ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    messages = [dict(row) for row in rows]
    return jsonify(messages)

if __name__ == "__main__":
    app.run(debug=True)

#Notes:
#GET /messages returns JSON list of stored messages (useful while developing). On production you should protect it with auth or remove it.