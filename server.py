import sqlite3, psycopg2
import flask
import json
from flask import jsonify, request, render_template,redirect, url_for, send_from_directory
import os
import psycopg2 as dpapi

url = "dbname='wezrrgcd' user='wezrrgcd' host='salt.db.elephantsql.com' password='gh4WaN_uVpfMTkAMF3AG-h2nXbbNr1FH' "
#url = os.getenv("DB_URL")
conn = dpapi.connect(url)
cursor = conn.cursor()
app = flask.Flask(__name__,template_folder="templates")


@app.route('/', methods=['GET'])
def home():
    user = request.args.get("username")

    cursor.execute("""SELECT pass1.* FROM (SELECT comment.commentid, comment.username, comment.usercomment, comment.commentdate, comment.commentlike, f.foodid, f.foodname, f.foodphoto FROM comment 
                          JOIN food f ON comment.foodid = f.foodid  ORDER BY commentlike DESC LIMIT 2) as pass1
                          UNION  
                          SELECT pass2.* FROM (SELECT comment.commentid, comment.username, comment.usercomment, comment.commentdate, comment.commentlike, d.dessertid, d.dessertname, d.dessertphoto FROM comment 
                          JOIN dessert d ON comment.dessertid = d.dessertid ORDER BY commentlike DESC LIMIT 1) as pass2
                          UNION 
                          SELECT pass3.* FROM (SELECT comment.commentid, comment.username, comment.usercomment, comment.commentdate, comment.commentlike, b.beverageid, b.beveragename, b.beveragephoto FROM comment 
                          JOIN beverage b ON comment.beverageid = b.beverageid ORDER BY commentlike DESC LIMIT 1) as pass3
                        """)
    data = cursor.fetchall()
    print(data)
    if data:
        return render_template("index.html", comments=data, username=user)
    else:
        return render_template("index.html")


@app.route('/profile', methods=['GET'])
def profile():
    userID = request.args.get("id")

    cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username FROM members 
                   INNER JOIN personaldata 
                   ON personaldata.memberid = members.memberid and members.memberid = %s """, (userID))


    data = cursor.fetchall()

    print(data)

    conn.commit()
    if data:
        return render_template("profile.html", datam=data)
    else:
        return render_template("profile.html")




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
            return redirect(url_for('profile',username=userName,id=data[0]))
        else:
            errors="Please try again!"
            return redirect(url_for('get_members',error=errors))
    else :
        return render_template("login-page.html")


@app.route('/new-password', methods=['GET'])
def newPass():

    userName = request.args.get("username")
    e_mail = request.args.get("email")
    answer = request.args.get("Answer")

    if userName and e_mail:
        cursor.execute("SELECT recoveryques, recoveryans FROM members where username=%s and e_mail=%s",(userName,e_mail))
        data = cursor.fetchall()
        conn.commit()
        
        if data:
            return render_template('new-password.html', email=e_mail, username=userName,datam=data)
            if answer:
                if(data[0][1] == answer):
                    return redirect(url_for('home',username=userName))

        else:
            return redirect(url_for('newPass'))

    else :
        return render_template("new-password.html")



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




@app.route('/food-menu', methods=['GET'])
def foods():
    cursor.execute("""
                SELECT food.foodid, food.foodphoto, food.foodname, qualification.cuisine, qualification.timing, qualification.qualificationid  FROM qualification
                INNER JOIN food
                ON food.qualificationid = qualification.qualificationid""")

    data = cursor.fetchall()
    print(data)

    if data:
        return render_template("food-menu.html", len = len(data), food=data)
    else:
        return render_template("food-menu.html")


@app.route('/drink-menu', methods=['GET'])
def drinks():

    cursor.execute("""
                SELECT beverage.beverageid, beverage.beveragephoto, beverage.beveragename,  qualification.cuisine,  qualification.timing, qualification.qualificationid FROM qualification
                INNER JOIN beverage
                ON beverage.qualificationid = qualification.qualificationid""")

    data = cursor.fetchall()
    print(data)

    if data:
        return render_template("drink-menu.html", len=len(data), drink=data)
    else:
        return render_template("drink-menu.html")

@app.route('/dessert-menu', methods=['GET'])
def desserts():

    cursor.execute("""
                SELECT dessert.dessertid,  dessert.dessertphoto, dessert.dessertname, qualification.cuisine, qualification.timing, qualification.qualificationid FROM qualification
                INNER JOIN dessert
                ON dessert.qualificationid = qualification.qualificationid""")

    data = cursor.fetchall()
    print(data)

    if data:
        return render_template("dessert-menu.html", len=len(data), dessert=data)
    else:
        return render_template("dessert-menu.html")


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