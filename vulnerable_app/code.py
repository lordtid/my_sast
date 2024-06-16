import sqlite3
from flask import Flask, request, jsonify, session
import hashlib

app = Flask(__name__)
app.secret_key = 'some_secret'


def connect_db():
    return sqlite3.connect('users.db')


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{hashed_password}')")
    conn.commit()
    conn.close()
    return jsonify({"status": "User registered!"})


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_password}'")
    user = cursor.fetchone()
    conn.close()

    if user:
        session['username'] = user[1]
        return jsonify({"status": "Logged in!"})
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route('/profile', methods=['GET'])
def profile():
    if 'username' in session:
        user_id = request.args.get('id')
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
        user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "Not logged in"}), 401


if __name__ == '__main__':
    app.run()