from flask import Flask, request, redirect, render_template_string
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'my_database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route('/')
def index():
    return "Welcome to our system!"

@app.route('/hello')
def say_hello():
    name = request.args.get("name", "World")
    return render_template_string('Hello, <strong>'+ name +'</strong>!')

@app.route('/execute')
def execute_command():
    command = request.args.get("cmd")
    result = os.system(command)
    return f'Command output: {result}'

@app.route('/users')
def show_user():
    user_id = request.args.get("id")
    cursor = get_db().cursor()
    cursor.execute("SELECT username FROM users WHERE id=" + user_id)
    username = cursor.fetchone()
    return f'Username: {username}'

@app.route('/redirect')
def redirect_user():
    url = request.args.get("url", "/")
    return redirect(url)

if __name__ == '__main__':
    app.run()