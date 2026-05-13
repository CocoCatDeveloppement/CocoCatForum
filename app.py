from flask import Flask, render_template, url_for, request, redirect, jsonify
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            pseudo TEXT NOT NULL,
            sujet TEXT NOT NULL,
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
    return render_template("index.html")

@app.route("/post", methods=["POST"])
def post():
    pseudo = request.form["pseudo"]
    sujet = request.form["sujet"]
    message = request.form["message"]
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO messages (pseudo, sujet, message, date) VALUES (%s, %s, %s, %s)",
        (pseudo, sujet, message, date)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/like", methods=["POST"])
def like():
    msg_id = request.json["id"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("UPDATE messages SET likes = likes + 1 WHERE id = %s", (msg_id,))
    conn.commit()

    cur.execute("SELECT likes FROM messages WHERE id = %s", (msg_id,))
    new_likes = cur.fetchone()[0]

    conn.close()

    return {"likes": new_likes}

@app.route("/messages_json")
def messages_json():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, pseudo, sujet, message, date, likes FROM messages ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    messages = [
        {
            "id": r[0],
            "pseudo": r[1],
            "sujet": r[2],
            "message": r[3],
            "date": r[4],
            "likes": r[5]
        }
        for r in rows
    ]

    return jsonify(messages)

if __name__ == "__main__":
    app.run(debug=True)

