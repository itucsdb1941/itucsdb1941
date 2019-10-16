import sqlite3
from sqlite3 import Error
import flask
from flask import jsonify

app = flask.Flask(__name__)


@app.route('/')
def login():
	conn = sqlite3.connect("bss.db",  check_same_thread=False)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM members")
	data = cursor.fetchall()
	for item in data:
		return jsonify(item)

if __name__ == '_main_':
    app.run(port=5000, debug=True)