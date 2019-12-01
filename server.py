import sqlite3, psycopg2
import flask
import json
from flask import jsonify, request, render_template,redirect, url_for, send_from_directory
import os
import psycopg2 as dpapi

url = "dbname='wezrrgcd' user='wezrrgcd' host='salt.db.elephantsql.com' password='gh4WaN_uVpfMTkAMF3AG-h2nXbbNr1FH' "
# url = os.getenv("DB_URL")
conn = dpapi.connect(url)
cursor = conn.cursor()
app = flask.Flask(__name__,template_folder="templates")


@app.route('/', methods=['GET'])
def home():
    user = request.args.get("username")
    return render_template("index.html", username=user)

@app.route('/foods-list', methods=['GET'])
def get_all_comment():
    res = []
    comment_keys = ["commentId", "userName", "score", "userComment", "commentDate", "commentLike", "foodID","foodName"];
    cursor.execute("""SELECT comment.commentID, comment.userName, comment.score, comment.userComment, comment.commentDate, comment.commentLike, food.foodID, food.foodName FROM food
                    INNER JOIN comment 
                    ON comment.foodID= food.foodID;
    """)
    data = cursor.fetchall()
    conn.commit()
    for i in data:
        res.append(dict(zip(comment_keys, i)))
    return jsonify(res)



@app.route('/sign-in', methods=['GET'])
def get_members():
    userName = request.args.get("username")
    passWord = request.args.get("password")
    if userName and passWord:
        if request.form.get("forgotPassword"):
            return render_template("index.html")
        cursor.execute("SELECT * FROM members where username=%s and userPassword=%s",(userName,passWord))
        data = cursor.fetchall()
        conn.commit()
        if data:
            return redirect(url_for('home',username=userName))
        else:
            errors="Please try again!"
            return redirect(url_for('get_members',error=errors))
    else :
        return render_template("login-page.html")


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


@app.route('/sign-up', methods=['GET','POST'])
def signUp():
    if request.method == 'POST':
        firstname = request.form.get("FirstName")
        lastname = request.form.get("LastName")
        email = request.form.get("Email")
        username = request.form.get("Username")
        password = request.form.get("Password")
        gender = request.form.get("Gender")
        birthdate = request.form.get("Birthdate")
        location = request.form.get("Location")
        rques = request.form.get("RecoveryQuestion")
        ranswer = request.form.get("RecoveryAnswer")

        if firstname and lastname and email and username and password and gender and birthdate and location and rques and ranswer:
            cursor.execute("INSERT INTO members(username, userpassword, e_mail, recoveryques, recoveryans) VALUES (%s, %s, %s, %s, %s)",(username, password, email, rques, ranswer) )
            conn.commit()
            cursor.execute("SELECT CURRVAL('members_memberid_seq')")
            sql = cursor.fetchone()
            cursor.execute("INSERT INTO personaldata (name, surname, birthdate, sex, location, memberid) "
                             "VALUES (%s,%s,%s,%s,%s,%s)", (firstname, lastname, birthdate, gender, location, sql[0]))
            conn.commit()
            return redirect(url_for('home',username=username))
        
    elif request.method == 'GET':
        return render_template("sign-page.html")


@app.route('/food-menu', methods=['GET','POST'])
def foods():
    res = []
    food_keys = ["foodID", "foodName", "foodPhoto", "cuisine","qualificationID", "timing"];

    cursor = conn.execute("""
                SELECT food.foodID, food.foodName, food.foodPhoto, qualification.cuisine, qualification.qualificationID, qualification.timing FROM qualification
                INNER JOIN food
                ON food.qualificationID = qualification.qualificationID""")

    data = cursor.fetchall()

    for i in data:
        res.append(dict(zip(food_keys, i)))
    return jsonify(res)

@app.route('/drink-menu', methods=['GET'])
def drinks():
    res = []
    drink_keys = ["beverageID", "beverageName", "beveragePhoto", "cuisine", "qualificationID", "timing"];

    cursor = conn.execute("""
                SELECT beverage.beverageID, beverage.beverageName, beverage.beveragePhoto, qualification.cuisine, qualification.qualificationID, qualification.timing FROM qualification
                INNER JOIN beverage
                ON beverage.qualificationID = qualification.qualificationID""")

    data = cursor.fetchall()

    for i in data:
        res.append(dict(zip(drink_keys, i)))
    return jsonify(res)

@app.route('/dessert-menu', methods=['GET'])
def desserts():
    res = []
    dessert_keys = ["dessertID", "dessertName", "dessertPhoto", "cuisine", "qualificationID", "timing"];

    cursor = conn.execute("""
                SELECT dessert.dessertID, dessert.dessertName, dessert.dessertPhoto, qualification.cuisine, qualification.qualificationID, qualification.timing FROM qualification
                INNER JOIN dessert
                ON dessert.qualificationID = qualification.qualificationID""")

    data = cursor.fetchall()

    for i in data:
        res.append(dict(zip(dessert_keys, i)))
    return jsonify(res)


@app.route('/recipe/food/<int:id>', methods=['GET'])
def foodRecipe(id):
    total = []
    res = []
    recipe = ["ID", "Name", "Photo", "Recipe", "ingreName", "unit", "amount", "cuisine", "qualificationID", "timing"]

    cursor = conn.execute("""
                SELECT food.foodID, food.foodName, food.foodPhoto, food.foodRecipe, ingredient.ingreName, ingredient.unit, ingredient.amount, qualification.cuisine, qualification.qualificationID, qualification.timing FROM food
                INNER JOIN  ingredient
                ON ingredient.foodID = food.foodID AND food.foodID = ?
                INNER JOIN qualification
                ON food.qualificationID = qualification.qualificationID""", [id])

    data = cursor.fetchall()

    for i in data:
        res.append(dict(zip(recipe, i)))

    res2 = []
    commentlist = ["ID", "userName", "comment", "date", "like", "dislike"]

    commentData = conn.execute("""SELECT comment.commentID, comment.userName,comment.userComment, comment.commentDate, comment.commentLike, comment.commentDislike FROM comment
                WHERE comment.foodID = ?""", [id])

    data2 = commentData.fetchall()

    for k in data2:
        res2.append(dict(zip(commentlist, k)))

    total.append(res)
    total.append(res2)

    return jsonify(total)

@app.route('/recipe/drink/<int:id>', methods=['GET'])
def drinkRecipe(id):

    res = []
    recipe = ["ID", "Name", "Photo", "Recipe", "ingreName", "unit", "amount", "cuisine", "qualificationID", "timing"]

    cursor = conn.execute("""
                SELECT beverage.beverageID, beverage.beverageName, beverage.beveragePhoto, beverage.beverageRecipe, ingredient.ingreName, ingredient.unit,  ingredient.amount, qualification.cuisine, qualification.qualificationID, qualification.timing FROM beverage
                INNER JOIN  ingredient
                ON ingredient.beverageID = beverage.beverageID AND beverage.beverageID = ?
                INNER JOIN qualification
                ON beverage.qualificationID = qualification.qualificationID""", [id])

    data = cursor.fetchall()
    for i in data:
        res.append(dict(zip(recipe, i)))

    return jsonify(res)


@app.route('/recipe/dessert/<int:id>', methods=['GET'])
def dessertRecipe(id):

    res = []
    recipe = ["ID", "Name", "Photo", "Recipe", "ingreName", "unit", "amount", "cuisine", "qualificationID", "timing"];

    cursor = conn.execute("""
                SELECT dessert.dessertID, dessert.dessertName, dessert.dessertPhoto, dessert.dessertRecipe, ingredient.ingreName, ingredient.unit,  ingredient.amount, qualification.cuisine, qualification.qualificationID, qualification.timing FROM dessert
                INNER JOIN  ingredient
                ON ingredient.dessertID = dessert.dessertID AND dessert.dessertID = ?
                INNER JOIN qualification
                ON dessert.qualificationID = qualification.qualificationID""", [id])

    data = cursor.fetchall()
    for i in data:
        res.append(dict(zip(recipe, i)))

    return jsonify(res)

if __name__ == '_main_':
    app.run(port=5000, debug=True)