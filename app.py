from flask import Flask, render_template, request
import requests
from werkzeug.security import check_password_hash, generate_password_hash
import json
import sqlite3
app = Flask(__name__)


def dbConnection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

with dbConnection() as connection:
    connection.execute('CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, score INTEGER NOT NULL)')

@app.route('/api/data', methods=['POST'])  
def api_data():
    if request.method == 'POST':
        data = request.json
        if not data:
            return 'No json', 400
        else:
            username = data.get('Username')
            score = int(data.get('Score'))
            with dbConnection() as connection:
                ifUser = connection.execute('SELECT * FROM scores WHERE username = ?', (username,)).fetchone()
                if ifUser:
                    if score > ifUser['score']:
                        connection.execute(f'UPDATE scores SET username = {username}, score = {score} WHERE username = ?', (username,))
                else:
                    connection.execute('INSERT INTO scores (username, score) VALUES  (?, ?)', (username, score))
        return 'JSON data received successfully!', 200
    else:
        return 'Method Not Allowed', 405
@app.route('/', methods=['POST', 'GET'])
def leaderboard():
    with dbConnection() as connection:
        scores = connection.execute('SELECT * FROM scores ORDER BY score DESC').fetchall()
    return render_template('leaderboard.html', scores=scores)

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0') 