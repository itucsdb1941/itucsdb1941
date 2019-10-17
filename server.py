import sqlite3
import flask
import json
from flask import jsonify
from flask_cors import CORS
from pkg_resources import require

app = flask.Flask(__name__)
CORS(app)
conn = sqlite3.connect("bss.db", check_same_thread=False)
cursor = conn.cursor()


@app.route('/')
def login():
    cursor.execute("SELECT * FROM personalData")
    data = cursor.fetchall()
    return data


@app.route('/foods-list', methods=['GET'])
def get_all_food():
    res = []
    food_keys = ["foodId", "foodName", "foodIngre", "foodRecipe", "foodPhoto", "qualificationID"];
    cursor.execute("SELECT * FROM food")
    data = cursor.fetchall()

    for i in data:
        res.append(dict(zip(food_keys, i)))
    return jsonify(res)


if __name__ == '_main_':
    app.run(port=5000, debug=True)
