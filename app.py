from flask import Flask, render_template, url_for, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("/tmp/forum.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo TEXT NOT NULL,
            message TEXT NOT NULL,
            date TEXT NOT NULL,
            likes INTEGER NOT NULL DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("/tmp/forum.db")
    cur = conn.cursor()
    cur.execute("SELECT id, pseudo, message, date, likes FROM messages ORDER BY id DESC")
    messages = cur.fetchall()
    conn.close()

    return render_template("index.html", messages=messages)

@app.route("/post", methods=["POST"])
def post():
    pseudo = request.form["pseudo"]
    message = request.form["message"]
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("/tmp/forum.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (pseudo, message, date) VALUES (?, ?, ?)",
        (pseudo, message, date)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/like", methods=["POST"])
def like():
    msg_id = request.json["id"]

    conn = sqlite3.connect("/tmp/forum.db")
    cur = conn.cursor()

    # On incrémente
    cur.execute("UPDATE messages SET likes = likes + 1 WHERE id = ?", (msg_id,))
    conn.commit()

    # On récupère le nouveau total
    cur.execute("SELECT likes FROM messages WHERE id = ?", (msg_id,))
    new_likes = cur.fetchone()[0]

    conn.close()

    return {"likes": new_likes}

if __name__ == "__main__":
    app.run(debug=True)
