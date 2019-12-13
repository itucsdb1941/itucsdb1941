import sqlite3, psycopg2
import flask
import json
from flask import jsonify, request, render_template,redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import psycopg2 as dpapi

url = "dbname='wezrrgcd' user='wezrrgcd' host='salt.db.elephantsql.com' password='gh4WaN_uVpfMTkAMF3AG-h2nXbbNr1FH' "


#url = os.getenv("DB_URL")
conn = dpapi.connect(url)
cursor = conn.cursor()
app = flask.Flask(__name__,template_folder="templates")

ingreList = [];
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'static/assets/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    print("filename",filename)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    user = request.args.get("username")

    cursor.execute("""SELECT pass1.* FROM (SELECT comment.commentid, comment.title, comment.usercomment, comment.commentdate, comment.commentlike, f.foodid, f.foodname, f.foodphoto FROM comment 
                          JOIN food f ON comment.foodid = f.foodid  ORDER BY commentlike DESC LIMIT 2) as pass1
                          UNION  
                          SELECT pass2.* FROM (SELECT comment.commentid, comment.title, comment.usercomment, comment.commentdate, comment.commentlike, d.dessertid, d.dessertname, d.dessertphoto FROM comment 
                          JOIN dessert d ON comment.dessertid = d.dessertid ORDER BY commentlike DESC LIMIT 1) as pass2
                          UNION 
                          SELECT pass3.* FROM (SELECT comment.commentid, comment.title, comment.usercomment, comment.commentdate, comment.commentlike, b.beverageid, b.beveragename, b.beveragephoto FROM comment 
                          JOIN beverage b ON comment.beverageid = b.beverageid ORDER BY commentlike DESC LIMIT 1) as pass3
                        """)

    data = cursor.fetchall()

   # cursor.execute("SELECT food.foodid, food.foodname, food.foodrecipe, food.foodphoto, food.foodtype, food.foodscore FROM food ORDER BY foodscore ASC LIMIT 1")
   # data2 = cursor.fetchall()
   # print(data2);
    if data :
        return render_template("index.html", comments =data, username=user)
    else:
        return render_template("index.html")


@app.route('/profile', methods=['GET'])
def profile():
    userID = request.args.get("id")

    cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username FROM members 
                   INNER JOIN personaldata 
                   ON personaldata.memberid = members.memberid and members.memberid = %s """, (userID))


    data = cursor.fetchall()
    #print(data)

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

    if data:
        return render_template("dessert-menu.html", len=len(data), dessert=data)
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
        data3 = cursor.fetchall();

        if data:
                return render_template("recipe.html",  len=len(data2), len2=len(data3), datam=data , comment=data2, ingre=data3)


    return render_template("recipe.html")


@app.route('/recipe/drink/<id>', methods=['GET'])
def drinkRecipe(id):

    cursor.execute("""
                SELECT beverage.beverageid, beverage.beveragename, beverage.beveragephoto, beverage.beveragerecipe, ingredient.ingrename, ingredient.unit,  ingredient.amount, qualification.cuisine, qualification.qualificationid, qualification.timing,  beverage.beveragedate FROM beverage
                INNER JOIN qualification
                ON beverage.qualificationid = qualification.qualificationid
                LEFT JOIN  ingredient
                ON ingredient.beverageid = beverage.beverageid AND beverage.beverageid = %s """, (id))

    data = cursor.fetchone()

    if data:
        return render_template("recipe.html", datam=data)
    else:
        return render_template("recipe.html")


@app.route('/recipe/dessert/<id>', methods=['GET'])
def dessertRecipe(id):

    cursor.execute("""
                SELECT dessert.dessertid, dessert.dessertname, dessert.dessertphoto, dessert.dessertrecipe, ingredient.ingrename, ingredient.unit,  ingredient.amount, qualification.cuisine, qualification.qualificationid, qualification.timing, dessert.dessertdate FROM dessert
                INNER JOIN qualification
                ON dessert.qualificationid = qualification.qualificationid
                LEFT JOIN  ingredient
                ON ingredient.dessertid = dessert.dessertid AND dessert.dessertid = %s""", (id))

    data = cursor.fetchone()

    if data:
        return render_template("recipe.html", datam=data)
    else:
        return render_template("recipe.html")

@app.route('/add-food', methods=['GET','POST'])
def post_food():

    if request.method == 'POST':
        membername = request.form.get("membername")
        foodname = request.form.get('foodname')
        foodtime = request.form.get('foodtime')
        foodcalorie = request.form.get('foodcalorie')
        foodcountry = request.form.get('foodcountry')
        foodtype = request.form.get('foodtype')
        fooddate = request.form.get('fooddate')
        foodserve = request.form.get('foodserve')
        foodrecipe = request.form.get('foodrecipe')
        foodcategory = request.form.get('foodcategory')
        foodphoto = request.form.get('foodphoto')

        if foodname and foodtime and foodcalorie and fooddate and foodserve and foodrecipe:
            cursor.execute("INSERT INTO qualification(cuisine, timing, category, calori, serve) VALUES(%s,%s,%s,%s,%s) RETURNING qualificationid",
                              (foodcountry, foodtime, foodcategory, foodcalorie, foodserve))
            qualificationId = cursor.fetchone()[0]
            conn.commit()

            cursor.execute("INSERT INTO food(foodname, foodrecipe, foodphoto, foodtype, qualificationid, memberid, fooddate) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING foodid" ,
                        (foodname, foodrecipe, foodphoto, foodtype, qualificationId, 1, fooddate))
            foodID = cursor.fetchone()[0]
            print("food" , foodID)
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

            cursor.execute("INSERT INTO ingredient(ingrename, unit, amount, allergenic, flavor, foodid) VALUES (%s,%s,%s,%s,%s,%s)",
                (ingrename, ingreunit, ingreamount, ingreallergenic, ingreFlavor, foodID))

            i = i + 1
            conn.commit()


        return render_template("add-food.html" , result="ok")
    else:
        return render_template("add-food.html" )



@app.route('/file-upload', methods=['POST'])
def upload_file():
    print(request.files)
    content_length = request.content_length
    print(f"Content_length : {content_length}")
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

if __name__ == '_main_':
    app.run(port=5000, debug=True)