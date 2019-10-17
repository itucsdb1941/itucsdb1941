import sqlite3
from sqlite3 import Error
import flask
from flask import jsonify

app = flask.Flask(__name__)
conn = sqlite3.connect("bss.db", check_same_thread=False)
cursor = conn.cursor()


@app.route('/')
def login():
    cursor.execute("SELECT * FROM personalData")
    data = cursor.fetchall()
    return data


@app.route('/foods-list')
def get_all_food():
    cursor.execute("SELECT * FROM food")
    data = cursor.fetchall()
    return jsonify(data)


if __name__ == '_main_':
    app.run(port=5000, debug=True)
