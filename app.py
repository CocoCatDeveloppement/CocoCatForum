from flask import Flask, render_template, url_for, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("forum.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo TEXT NOT NULL,
            message TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("forum.db")
    cur = conn.cursor()
    cur.execute("SELECT pseudo, message, date FROM messages ORDER BY id DESC")
    messages = cur.fetchall()
    conn.close()

    return render_template("index.html", messages=messages)


@app.route("/post", methods=["POST"])
def post():
    pseudo = request.form["pseudo"]
    message = request.form["message"]

    conn = sqlite3.connect("forum.db")
    cur = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute(
    "INSERT INTO messages (pseudo, message, date) VALUES (?, ?, ?)",
    (pseudo, message, date)
)

    conn.commit()
    conn.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
