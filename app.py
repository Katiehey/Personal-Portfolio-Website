# app.py
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import secrets
import requests
import os
import sqlite3
from pathlib import Path

app = Flask(__name__, static_folder="static", template_folder="templates")
DB_PATH = Path("instance/contact_messages.db")
app.secret_key = secrets.token_hex(16)
# Get your PAT from an environment variable (as we discussed previously)
GITHUB_TOKEN = os.environ.get('GITHUB_PAT') 

def get_db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        pwd = request.form.get("password", "")
        from config import ADMIN_PASSWORD
        if pwd == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_messages"))
        return render_template("admin_login.html", error="Wrong password")
    return render_template("admin_login.html")

@app.route("/admin/messages")
def admin_messages():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn = get_db_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM messages ORDER BY created_at DESC")
    messages = c.fetchall()
    conn.close()

    return render_template("admin_messages.html", messages=messages)


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

# Get your PAT from an environment variable (as we discussed previously)
GITHUB_TOKEN = os.environ.get('GITHUB_PAT') 

if GITHUB_TOKEN is None:
    # Handle the error if you don't set the token
    raise ValueError("GitHub PAT not set.")

@app.route("/github-projects")
def github_projects():
    username = "Katiehey"

    url = f"https://api.github.com/users/{username}/repos"
    res = requests.get(url)
    data = res.json()

    projects = []

    # Add authentication headers to the request
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json" # Good practice to specify API version
    }

    res = requests.get(url, headers=headers)
    res.raise_for_status() # This raises an exception if the request fails (e.g., if the token is bad)
    data = res.json()


    for repo in data:
        projects.append({
            "title": repo["name"],
            "desc": repo["description"] or "No description",
            "tech": [],
            "github": repo["html_url"],
            # Add this line to capture the URL we added in Step 1
            "live_url": repo["homepage"] or None # Use None if no homepage is set
        })

    return jsonify(projects)


if __name__ == "__main__":
    app.run(debug=True)

#Notes:
#GET /messages returns JSON list of stored messages (useful while developing). On production you should protect it with auth or remove it.