import sqlite3, psycopg2
import flask
import json
from flask import jsonify, request, render_template,redirect, url_for, send_from_directory, session
from flask import jsonify, request, render_template,redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

import os
import psycopg2 as dpapi

url = "dbname='wezrrgcd' user='wezrrgcd' host='salt.db.elephantsql.com' password='gh4WaN_uVpfMTkAMF3AG-h2nXbbNr1FH' "
# url = os.getenv("DB_URL")
conn = dpapi.connect(url)
cursor = conn.cursor()
app = flask.Flask(__name__,template_folder="templates")
app.secret_key = "sdsgchg"

ingreList = [];
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'static/assets/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    print("filename",filename)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    cursor.execute("""SELECT comment.commentid, comment.title, comment.usercomment, comment.commentdate, comment.commentlike, f.foodid, f.foodname, f.foodphoto, m.username FROM comment 
                          JOIN food f ON comment.foodid = f.foodid JOIN members m on comment.memberid = m.memberid  ORDER BY comment.commentlike DESC NULLS LAST LIMIT 2     
                        """)
    data = cursor.fetchall()

    cursor.execute("""SELECT comment.commentid, comment.title, comment.usercomment, comment.commentdate, comment.commentlike, d.dessertid, d.dessertname, d.dessertphoto, m.username FROM comment 
                          JOIN dessert d ON comment.dessertid = d.dessertid JOIN members m on comment.memberid = m.memberid ORDER BY comment.commentlike DESC NULLS LAST """)
    data2 = cursor.fetchone()

    cursor.execute("""SELECT comment.commentid, comment.title, comment.usercomment, comment.commentdate, comment.commentlike, b.beverageid, b.beveragename, b.beveragephoto, m.username FROM comment 
                              JOIN beverage b ON comment.beverageid = b.beverageid JOIN members m on comment.memberid = m.memberid ORDER BY comment.commentlike DESC NULLS LAST """)
    data3 = cursor.fetchone()

    cursor.execute("""SELECT  food.foodid, food.foodname, food.foodrecipe, food.foodphoto, food.fooddate FROM food 
                            ORDER BY food.fooddate ASC NULLS LAST """)
    data4 = cursor.fetchone()

    cursor.execute("""SELECT  dessert.dessertid, dessert.dessertname, dessert.dessertrecipe, dessert.dessertphoto, dessert.dessertdate FROM dessert 
                                ORDER BY dessert.dessertdate ASC NULLS LAST """)
    data5 = cursor.fetchone()

    cursor.execute("""SELECT  beverage.beverageid, beverage.beveragename, beverage.beveragerecipe, beverage.beveragephoto, beverage.beveragedate FROM beverage 
                                ORDER BY beverage.beveragedate ASC NULLS LAST """)
    data6 = cursor.fetchone()

   # cursor.execute("SELECT food.foodid, food.foodname, food.foodrecipe, food.foodphoto, food.foodtype, food.foodscore FROM food ORDER BY foodscore ASC LIMIT 1")
   # data2 = cursor.fetchall()

    username = ""
    if 'username' in session:
        username = session['username']

    if data and data2 and data3 and data4 and data5 and data6:
        return render_template("index.html", comment1 =data[0], comment2=data2, comment3=data3, comment4 =data[1], beverage=data6, food= data4, dessert= data5, username=username)
    else:
        return render_template("index.html")

@app.route('/profile', methods=['GET'])
def profile():

    if "id" in session:
        print(session["id"])
        cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username FROM members 
                       INNER JOIN personaldata 
                       ON personaldata.memberid = members.memberid and members.memberid = %s """, str(session["id"]))
        data = cursor.fetchall()


        cursor.execute(""" SELECT food.foodid, food.foodphoto, food.foodname, qualification.cuisine, qualification.timing, qualification.qualificationid, food.foodrecipe FROM qualification
                    INNER JOIN food
                    ON food.qualificationid = qualification.qualificationid and food.memberid = %s""", str(session["id"]))

        foods = cursor.fetchall()

        cursor.execute(""" SELECT dessert.dessertid, dessert.dessertphoto, dessert.dessertname, qualification.cuisine, qualification.timing, qualification.qualificationid, dessert.dessertrecipe FROM qualification
                        INNER JOIN dessert
                        ON dessert.qualificationid = qualification.qualificationid and dessert.memberid = %s""", str(session["id"]))

        desserts = cursor.fetchall()

        cursor.execute(""" SELECT beverage.beverageid, beverage.beveragephoto, beverage.beveragename, qualification.cuisine, qualification.timing, qualification.qualificationid, beverage.beveragerecipe FROM qualification
                        INNER JOIN beverage
                        ON beverage.qualificationid = qualification.qualificationid and beverage.memberid = %s""", str(session["id"]))

        drinks = cursor.fetchall()

        if data or foods or drinks or desserts:
            return render_template("profile.html", authority=session["authority"] , datam=data, foodlen =len(foods), drinklen =len(drinks), dessertlen=len(desserts), food=foods, dessert=desserts, drink=drinks)
        else:
            return render_template("profile.html")
    else:
       return render_template("index.html")

@app.route('/all-contacts', methods=['GET' , 'POST'])
def all_contacts():
    if request.method == 'POST':
        contactid = request.form.get('contactid')
        print(contactid)
        cursor.execute("DELETE FROM contact WHERE contactid=%s" , str(contactid))
        return redirect(url_for('all_contacts'))
    else:
        if "authority" in session:
            authority = session['authority']
            cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username FROM members 
                              INNER JOIN personaldata 
                              ON personaldata.memberid = members.memberid and members.memberid = %s """,
                           str(session["id"]))
            data = cursor.fetchall()

            if authority == 'admin':
                cursor.execute("SELECT contactid, message, date, title, category, e_mail FROM contact")
                contacts = cursor.fetchall()

            if contacts:
                return render_template("show-contacts.html",authority=session["authority"] , contact=contacts, datam=data, contactlen=len(contacts))
            else:
                return render_template("show-contacts.html",authority=session["authority"] ,  datam=data, contactlen=0, result="No contact..")
        else :
            return render_template(url_for("profile"))


@app.route('/sign-in', methods=['GET'])
def get_members():
    userName = request.args.get("username")
    passWord = request.args.get("password")

    if userName and passWord:
        if request.form.get("forgotPassword"):
            return render_template("index.html")
        cursor.execute("SELECT * FROM members where username=%s and userPassword=%s",(userName,passWord))
        data = cursor.fetchone()
        conn.commit()

        if data:
            session["username"]= userName
            session["id"] = data[0]
            session['authority'] = data[6]
            return redirect(url_for('profile'))
        else:
            errors="Please try again!"
            return redirect(url_for('get_members',error=errors))
    else :
        return render_template("login-page.html")

@app.route('/logout', methods=['GET'])
def logout():
   if 'id' in session:
        session.pop('id')
   if 'username' in session:
       session.pop('username')
   return redirect(url_for('home'))


@app.route('/new-password', methods=['GET'])
def newPass():
    if 'id' in session:
        return redirect(url_for('home'))
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
    if 'id' in session:
        return redirect(url_for('home'))

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
    username = ""
    if 'username' in session:
        username = session['username']
    if data:
        return render_template("food-menu.html", len = len(data), food=data, username=username)
    else:
        return render_template("food-menu.html")


@app.route('/drink-menu', methods=['GET'])
def drinks():

    cursor.execute("""
                SELECT beverage.beverageid, beverage.beveragephoto, beverage.beveragename,  qualification.cuisine,  qualification.timing, qualification.qualificationid FROM qualification
                INNER JOIN beverage
                ON beverage.qualificationid = qualification.qualificationid""")

    data = cursor.fetchall()
    username = ""
    if 'username' in session:
        username = session['username']
    if data:
        return render_template("drink-menu.html", len=len(data), drink=data, username=username)
    else:
        return render_template("drink-menu.html")

@app.route('/dessert-menu', methods=['GET'])
def desserts():

    cursor.execute("""
                SELECT dessert.dessertid,  dessert.dessertphoto, dessert.dessertname, qualification.cuisine, qualification.timing, qualification.qualificationid FROM qualification
                INNER JOIN dessert
                ON dessert.qualificationid = qualification.qualificationid""")

    data = cursor.fetchall()
    username = ""
    if 'username' in session:
        username = session['username']
    if data:
        return render_template("dessert-menu.html", len=len(data), dessert=data, username=username)
    else:
        return render_template("dessert-menu.html")


@app.route('/recipe/food/<id>', methods=['GET', 'POST'])
def foodRecipe(id):

    if request.method == 'POST':
        mytitle = request.form.get("title")
        mycomment = request.form.get("comment")
        print(mytitle)
        print(mycomment)
        if mycomment and mytitle:
            cursor.execute("INSERT INTO comment(usercomment, title, foodid) VALUES (%s, %s, %s)",(mycomment, mytitle,id))
            conn.commit()
            return redirect(url_for('foodRecipe'))
    else:
        cursor.execute("""
                    SELECT food.foodid, food.foodname, food.foodphoto, food.foodrecipe, ingredient.ingrename, ingredient.unit, ingredient.amount, qualification.cuisine, qualification.qualificationid, qualification.timing, food.fooddate FROM food
                    INNER JOIN qualification
                    ON food.qualificationid = qualification.qualificationid
                    INNER JOIN  ingredient
                    ON ingredient.foodid = food.foodid AND food.foodid = %s""", (id))
        data = cursor.fetchone()
        foodid = data[0]

        cursor.execute("SELECT comment.usercomment, comment.commentdate, members.username, comment.title FROM comment INNER JOIN members ON comment.memberid = members.memberid where comment.foodid = %s ", (foodid,))
        data2 = cursor.fetchall()

        cursor.execute("SELECT ingredient.ingrename, ingredient.unit, ingredient.amount FROM ingredient INNER JOIN food ON ingredient.foodid = food.foodid AND food.foodid = %s """,(id))
        data3 = cursor.fetchall()

        username = ""
        if 'username' in session:
            username = session['username']
        if data:
                return render_template("recipe.html",  len=len(data2), len2=len(data3), datam=data , comment=data2, ingre=data3, username=username)


    return render_template("recipe.html")


@app.route('/recipe/drink/<id>', methods=['GET', 'POST'])
def drinkRecipe(id):

    if request.method == 'POST':
        mytitle = request.form.get("title")
        mycomment = request.form.get("comment")
        print(mytitle)
        print(mycomment)
        if mycomment and mytitle:
            cursor.execute("INSERT INTO comment(usercomment, title, beverageid) VALUES (%s, %s, %s)",
                           (mycomment, mytitle, id))
            conn.commit()
            return redirect(url_for('drinkRecipe'))
    else:
        cursor.execute("""
                            SELECT beverage.beverageid, beverage.beveragename, beverage.beveragephoto, beverage.beveragerecipe, ingredient.ingrename, ingredient.unit, ingredient.amount, qualification.cuisine, qualification.qualificationid, qualification.timing, beverage.beveragedate FROM beverage
                            INNER JOIN qualification
                            ON beverage.qualificationid = qualification.qualificationid
                            INNER JOIN  ingredient
                            ON ingredient.beverageid = beverage.beverageid AND beverage.beverageid = %s""", (id))
        data = cursor.fetchone()
        print(data)
        drinkid = data[0]

        cursor.execute(
            "SELECT comment.usercomment, comment.commentdate, members.username, comment.title FROM comment INNER JOIN members ON comment.memberid = members.memberid where comment.beverageid = %s ",
            (drinkid,))
        data2 = cursor.fetchall()

        cursor.execute(
            "SELECT ingredient.ingrename, ingredient.unit, ingredient.amount FROM ingredient INNER JOIN beverage ON ingredient.foodid = beverage.beverageid AND beverage.beverageid = %s """,
            (id))
        data3 = cursor.fetchall()

        username = ""
        if 'username' in session:
            username = session['username']

        if data:
            return render_template("recipe.html", len=len(data2), len2=len(data3), datam=data, comment=data2,
                                   ingre=data3, username=username)

    return render_template("recipe.html")




@app.route('/recipe/dessert/<id>', methods=['GET', 'POST'])
def dessertRecipe(id):

    if request.method == 'POST':
        mytitle = request.form.get("title")
        mycomment = request.form.get("comment")
        print(mytitle)
        print(mycomment)
        if mycomment and mytitle:
            cursor.execute("INSERT INTO comment(usercomment, title, dessertid, memberid) VALUES (%s, %s, %s,1)",
                           (mycomment, mytitle, id))
            conn.commit()
            return redirect(url_for('dessertRecipe', id=id))
    else:
        cursor.execute("""
                            SELECT dessert.dessertid, dessert.dessertname, dessert.dessertphoto, dessert.dessertrecipe, ingredient.ingrename, ingredient.unit, ingredient.amount, qualification.cuisine, qualification.qualificationid, qualification.timing, dessert.dessertdate FROM dessert
                            INNER JOIN qualification
                            ON dessert.qualificationid = qualification.qualificationid
                            INNER JOIN  ingredient
                            ON dessert.dessertid = dessert.dessertid AND dessert.dessertid = %s""", (id))
        data = cursor.fetchone()
        print(data)
        dessertid = data[0]

        cursor.execute(
            "SELECT comment.usercomment, comment.commentdate, members.username, comment.title FROM comment INNER JOIN members ON comment.memberid = members.memberid where comment.dessertid = %s ",
            (dessertid,))
        data2 = cursor.fetchall()
        print(data2)

        cursor.execute(
            "SELECT ingredient.ingrename, ingredient.unit, ingredient.amount FROM ingredient INNER JOIN dessert ON ingredient.dessertid = dessert.dessertid AND dessert.dessertid = %s """,
            (id))
        data3 = cursor.fetchall()

        username = ""
        if 'username' in session:
            username = session['username']
        if data:
            return render_template("recipe.html", len=len(data2), len2=len(data3), datam=data, comment=data2,
                                   ingre=data3, username=username)

    return render_template("recipe.html")


@app.route('/add-recipe', methods=['GET','POST'])
def post_food():
    qualificationId = 0
    if request.method == 'POST':
        memberid = session["id"]
        name = request.form.get('recipename')
        time = request.form.get('recipetime')
        calorie = request.form.get('recipecalorie')
        country = request.form.get('recipecountry')
        type = request.form.get('recipetype')
        date = request.form.get('recipedate')
        serve = request.form.get('recipeserve')
        recipe = request.form.get('recipes')
        category = request.form.get('recipecategory')
        photo = request.form.get('recipephoto')
        recipeType = request.form.get('recipeType')
        print(name , time , calorie, date , country, serve , recipe)
        if name and time and calorie and date and serve and recipe:
            print("Asdfsdf")
            cursor.execute("INSERT INTO qualification(cuisine, timing, category, calori, serve) VALUES(%s,%s,%s,%s,%s) RETURNING qualificationid",
                              (country, time, category, calorie, serve))
            qualificationId = cursor.fetchone()[0]
            conn.commit()

            id=0
            if recipeType == "food":
                cursor.execute("INSERT INTO food(foodname, foodrecipe, foodphoto, foodtype, qualificationid, memberid, fooddate) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING foodid" ,
                            (name, recipe, photo, type, qualificationId, memberid, date))
                id = cursor.fetchone()[0]
                print("food" , id)
                conn.commit()
            elif recipeType == "beverage":
                cursor.execute(
                    "INSERT INTO beverage(beveragename, beveragerecipe, beveragephoto, beveragetype, qualificationid, memberid, beveragedate) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING foodid",
                    (name, recipe, photo, type, qualificationId, memberid, date))
                id = cursor.fetchone()[0]
                print("beverage", id)
                conn.commit()
            elif recipeType == "beverage":
                cursor.execute(
                    "INSERT INTO dessert(dessertname, dessertrecipe, dessertphoto, desserttype, qualificationid, memberid, dessertdate) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING foodid",
                    (name, recipe, photo, type, qualificationId, memberid, date))
                id = cursor.fetchone()[0]
                print("dessert", id)
                conn.commit()

            i = 0
            while request.form.get("ingrename" + str(i)) :
                ingreFlavor = ""
                ingreallergenic = False
                ingrename = request.form.get("ingrename" + str(i))
                ingreamount = request.form.get("ingreamount" + str(i))
                ingreunit = request.form.get("ingreunit" + str(i))
                if request.form.get("ingreallegernic" + str(i)):
                    ingreallergenic = True
                if request.form.get("flavorHot" + str(i)):
                    ingreFlavor = ingreFlavor + "Hot"
                if request.form.get("flavorSweet" + str(i)):
                    ingreFlavor = ingreFlavor + ",Sweet"
                if request.form.get("flavorSour" + str(i)):
                    ingreFlavor = ingreFlavor + ",Sour"
                if recipeType == "food":
                    cursor.execute("INSERT INTO ingredient(ingrename, unit, amount, allergenic, flavor, foodid) VALUES (%s,%s,%s,%s,%s,%s)",
                        (ingrename, ingreunit, ingreamount, ingreallergenic, ingreFlavor, id))
                elif recipeType == "beverage":
                    cursor.execute(
                        "INSERT INTO ingredient(ingrename, unit, amount, allergenic, flavor, beverageid) VALUES (%s,%s,%s,%s,%s,%s)",
                        (ingrename, ingreunit, ingreamount, ingreallergenic, ingreFlavor, id))
                elif recipeType == "dessert":
                    cursor.execute(
                        "INSERT INTO ingredient(ingrename, unit, amount, allergenic, flavor, dessertid) VALUES (%s,%s,%s,%s,%s,%s)",
                        (ingrename, ingreunit, ingreamount, ingreallergenic, ingreFlavor, id))
                i = i + 1
                conn.commit()

            myResult = recipeType + "added successfully."
            return render_template("add-recipe.html" , result=myResult)
    else:
        if "id" in session:
            print(session["id"])
            cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username FROM members 
                            INNER JOIN personaldata 
                            ON personaldata.memberid = members.memberid and members.memberid = %s """,
                           str(session["id"]))
        data = cursor.fetchall()
        return render_template("add-recipe.html" , datam=data)


@app.route('/change-recipe/food/<id>', methods=['GET','POST'])
def change_food(id):
    qualificationId = 0
    if request.method == 'POST':
        memberid = session["id"]
        qualificationid = request.form.get('qualificationid')
        name = request.form.get('recipename')
        time = request.form.get('recipetime')
        calorie = request.form.get('recipecalorie')
        country = request.form.get('recipecountry')
        type = request.form.get('recipetype')
        date = request.form.get('recipedate')
        serve = request.form.get('recipeserve')
        recipe = request.form.get('recipes')
        category = request.form.get('recipecategory')
        recipeType = request.form.get('recipeType')
        print(name , time , calorie, date , country, serve , recipe)
        cursor.execute("UPDATE qualification SET cuisine = %s , timing = %s, category = %s, calori = %s, serve= %s WHERE qualificationid = %s",
                        (country, time, category, calorie, serve, qualificationid))
        cursor.execute(
            "UPDATE food SET foodname = %s , foodrecipe = %s, foodtype = %s WHERE foodid = %s",
            (name, recipe, type, id))

        i=0
        while request.form.get("ingrename" + str(i)):
            ingreid = request.form.get("ingredientid"+ str(i))
            ingrename = request.form.get("ingrename" + str(i))
            ingreamount = request.form.get("ingreamount" + str(i))
            ingreunit = request.form.get("ingreunit" + str(i))
            print(ingrename,ingreamount,ingreunit)
            cursor.execute(
                "UPDATE ingredient SET ingrename = %s , unit = %s, amount = %s WHERE foodid = %s and ingredientid=%s ",
                (ingrename, ingreunit, ingreamount, id , ingreid))
            conn.commit()
            i=i+1
        conn.commit()

        return redirect(url_for("profile"))
    else:
        cursor.execute(""" SELECT food.foodname, qualification.cuisine, qualification.calori, qualification.serve,  qualification.timing, qualification.category,food.foodrecipe, food.foodtype, qualification.qualificationid FROM qualification
                    INNER JOIN food
                    ON food.qualificationid = qualification.qualificationid and food.foodid=%s""", (id))
        foods = cursor.fetchone()
        print(foods[4])
        cursor.execute("SELECT ingredient.ingrename, ingredient.unit, ingredient.amount, ingredient.ingredientid FROM ingredient INNER JOIN food ON ingredient.foodid = food.foodid AND food.foodid = %s """,(id))
        data3 = cursor.fetchall()
        print(data3)
        cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username FROM members 
                           INNER JOIN personaldata 
                           ON personaldata.memberid = members.memberid and members.memberid = %s """,
                       str(session["id"]))
        memberdata = cursor.fetchall()
        return render_template("change-recipe.html", datam=memberdata, data=foods , ingre=data3 , ingrelen=len(data3))


@app.route('/change-recipe/dessert/<id>', methods=['GET','POST'])
def change_dessert(id):
    qualificationId = 0
    if request.method == 'POST':
        memberid = session["id"]
        qualificationid = request.form.get('qualificationid')
        name = request.form.get('recipename')
        time = request.form.get('recipetime')
        calorie = request.form.get('recipecalorie')
        country = request.form.get('recipecountry')
        type = request.form.get('recipetype')
        date = request.form.get('recipedate')
        serve = request.form.get('recipeserve')
        recipe = request.form.get('recipes')
        category = request.form.get('recipecategory')
        recipeType = request.form.get('recipeType')
        print(name , time , calorie, date , country, serve , recipe)
        cursor.execute("UPDATE qualification SET cuisine = %s , timing = %s, category = %s, calori = %s, serve= %s WHERE qualificationid = %s",
                        (country, time, category, calorie, serve, qualificationid))
        cursor.execute(
            "UPDATE dessert SET dessertname = %s , dessertrecipe = %s, desserttype = %s WHERE dessertid = %s",
            (name, recipe, type, id))

        i=0
        while request.form.get("ingrename" + str(i)):
            ingreid = request.form.get("ingredientid"+ str(i))
            ingrename = request.form.get("ingrename" + str(i))
            ingreamount = request.form.get("ingreamount" + str(i))
            ingreunit = request.form.get("ingreunit" + str(i))
            print(ingrename,ingreamount,ingreunit)
            cursor.execute(
                "UPDATE ingredient SET ingrename = %s , unit = %s, amount = %s WHERE dessertid = %s and ingredientid=%s ",
                (ingrename, ingreunit, ingreamount, id , ingreid))
            conn.commit()
            i=i+1
        conn.commit()

        return redirect(url_for("profile"))
    else:
        cursor.execute(""" SELECT dessert.dessertname, qualification.cuisine, qualification.calori, qualification.serve,  qualification.timing, qualification.category,dessert.dessertrecipe, dessert.desserttype, qualification.qualificationid FROM qualification
                    INNER JOIN dessert
                    ON dessert.qualificationid = qualification.qualificationid and dessert.dessertid=%s""", (id))
        desserts = cursor.fetchone()
        cursor.execute("SELECT ingredient.ingrename, ingredient.unit, ingredient.amount, ingredient.ingredientid FROM ingredient INNER JOIN dessert ON ingredient.dessertid = dessert.dessertid AND dessert.dessertid = %s """,(id))
        data3 = cursor.fetchall()
        print(data3)
        cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username FROM members 
                           INNER JOIN personaldata 
                           ON personaldata.memberid = members.memberid and members.memberid = %s """,
                       str(session["id"]))
        memberdata = cursor.fetchall()
        return render_template("change-recipe.html", datam=memberdata, data=desserts , ingre=data3 , ingrelen=len(data3))


@app.route('/change-recipe/drink/<id>', methods=['GET','POST'])
def change_drink(id):
    qualificationId = 0
    if request.method == 'POST':
        memberid = session["id"]
        qualificationid = request.form.get('qualificationid')
        name = request.form.get('recipename')
        time = request.form.get('recipetime')
        calorie = request.form.get('recipecalorie')
        country = request.form.get('recipecountry')
        type = request.form.get('recipetype')
        date = request.form.get('recipedate')
        serve = request.form.get('recipeserve')
        recipe = request.form.get('recipes')
        category = request.form.get('recipecategory')
        recipeType = request.form.get('recipeType')
        print(name , time , calorie, date , country, serve , recipe)
        cursor.execute("UPDATE qualification SET cuisine = %s , timing = %s, category = %s, calori = %s, serve= %s WHERE qualificationid = %s",
                        (country, time, category, calorie, serve, qualificationid))
        cursor.execute(
            "UPDATE beverage SET beveragename = %s , beveragerecipe = %s, beveragetype = %s WHERE beverageid = %s",
            (name, recipe, type, id))

        i=0
        while request.form.get("ingrename" + str(i)):
            ingreid = request.form.get("ingredientid"+ str(i))
            ingrename = request.form.get("ingrename" + str(i))
            ingreamount = request.form.get("ingreamount" + str(i))
            ingreunit = request.form.get("ingreunit" + str(i))
            print(ingrename,ingreamount,ingreunit)
            cursor.execute(
                "UPDATE ingredient SET ingrename = %s , unit = %s, amount = %s WHERE beverageid = %s and ingredientid=%s ",
                (ingrename, ingreunit, ingreamount, id , ingreid))
            conn.commit()
            i=i+1
        conn.commit()

        return redirect(url_for("profile"))
    else:
        cursor.execute(""" SELECT beverage.beveragename, qualification.cuisine, qualification.calori, qualification.serve,  qualification.timing, qualification.category,beverage.beveragerecipe, beverage.beveragetype, qualification.qualificationid FROM qualification
                    INNER JOIN beverage
                    ON beverage.qualificationid = qualification.qualificationid and beverage.beverageid=%s""", (id))
        drinks= cursor.fetchone()

        cursor.execute("SELECT ingredient.ingrename, ingredient.unit, ingredient.amount, ingredient.ingredientid FROM ingredient INNER JOIN beverage ON ingredient.beverageid = beverage.beverageid AND beverage.beverageid = %s """,(id))
        data3 = cursor.fetchall()
        print(data3)
        cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username FROM members 
                           INNER JOIN personaldata 
                           ON personaldata.memberid = members.memberid and members.memberid = %s """,
                       str(session["id"]))
        memberdata = cursor.fetchall()
        return render_template("change-recipe.html", datam=memberdata, data=drinks , ingre=data3 , ingrelen=len(data3))


@app.route('/file-upload', methods=['POST'])
def upload_file():
    print(request.files)
    content_length = request.content_length
    print("Content_length : {content_length}")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return jsonify ({ " text" : " No File"})

        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return jsonify ({ " text" : " File hasn't selected"})
        print(allowed_file(file.filename))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify ({ " text" : " File Uploaded Successfully"})
        return ""


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        print("abcd")
        message = request.form.get("message")
        title = request.form.get("title")
        category = request.form.get("category")
        mail = request.form.get("e_mail")
        date = request.form.get("date")
        print(message, title, category, mail)
        if message and title and category and mail:
            cursor.execute(
                "INSERT INTO contact(message, title, category, e_mail, date) VALUES (%s, %s, %s, %s, %s)",
                (message, title, category, mail, date))
            conn.commit()
            return redirect(url_for('home'))

        else:
            return render_template("contact.html")
    else:
        return render_template("contact.html")


if __name__ == '_main_':
    app.run(port=5000, debug=True)