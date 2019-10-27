import sqlite3
import flask
import json
import requests
from flask import jsonify, render_template
from flask_wtf import FlaskForm
from flask_cors import CORS
from pkg_resources import require

app = flask.Flask(__name__)
CORS(app)
conn = sqlite3.connect("bss.db", check_same_thread=False)
cursor = conn.cursor()



@app.route('/')
def login():
    res = []
    cursor.execute("SELECT * FROM members")
    data = cursor.fetchall()

    for i in data:
        res.append(dict(zip(data, i)))

    return jsonify(data)

@app.route('/foods-list', methods=['GET'])
def get_all_food():
    res = []
    food_keys = ["foodId", "foodName", "foodIngre", "foodRecipe", "foodPhoto", "qualificationID"];
    cursor.execute("SELECT * FROM food")
    data = cursor.fetchall()

    for i in data:
        res.append(dict(zip(food_keys, i)))
    return jsonify(res)

@app.route('/login-page', methods=['GET','POST'])
def get_members():
    res = []
    member_keys = ["memberID", "username", "userPassword", "e_mail", "recoveryQues", "recoveryAns"];
    cursor.execute("SELECT * FROM members")
    data = cursor.fetchall()

    for i in data:
        res.append(dict(zip(member_keys, i)))
    return jsonify(res)

@app.route('/new-password/<int:id>', methods=['GET'])
def newPass(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM username WHERE id = {id}")
    old_data = cursor.fetchone()
    data = cursor.fetchall()

    return jsonify(data)

if __name__ == '_main_':
    app.run(port=5000, debug=True)


