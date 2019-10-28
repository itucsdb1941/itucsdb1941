
import sqlite3
import flask
import json
from flask import jsonify, request
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
conn = sqlite3.connect("bss.db", check_same_thread=False)
cursor = conn.cursor()


@app.route('/')
def login():
    res = []
    cursor.execute("SELECT * FROM personalData")
    data = cursor.fetchall()
    if data:
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


@app.route('/new-password', methods=['GET'])
def newPass():
    data = request.data
    if data:
        item = json.loads(data)
        for i in item:
            cursor.execute("SELECT * FROM members WHERE username =?", [i['UserName']])
            old_data = cursor.fetchone()
            return jsonify(old_data)
    else:
        return jsonify("empty")


@app.route('/sign-register', methods=['GET', 'POST'])
def post_sign():
    data = request.data
    if data:
        item = json.loads(data)
        for i in item:
            cursor.execute("INSERT INTO members (username, userPassword, e_mail, recoveryQues, recoveryAns) VALUES (?,?, ?,?,?)", (i['UserName'], i['Password'], i['Email'], i['RecoveryQuestion'], i['RecoveryAnswer']))
            cursor.execute("SELECT memberID FROM members WHERE username = ?", [i['UserName']])
            sql = cursor.fetchone()
            cursor.execute("INSERT INTO personalData (name, surname, birthdate, sex, location, memberID) "
                                       "VALUES (?,?,?,?,?,?)", (i['FirstName'], i['LastName'], i['Birthdate'], i['Gender'], i['Location'], sql[0]))
            conn.commit()

            return jsonify("ok")
    else:
        return "empty"



if __name__ == '_main_':
    app.run(port=5000, debug=True)
