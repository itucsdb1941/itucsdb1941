Parts Implemented by Rumeysa Nur Arslan
================================




**explain the technical structure of your code**

**to include a code listing, use the following example**:

  
   .. code-block:: python

      
	  @app.route('/all-contacts', methods=['GET' , 'POST'])
	  def all_contacts():
	  	  conn = dpapi.connect(url)
	  	  cursor = conn.cursor()
		  if request.method == 'POST':
			  contactid = request.form.get('contactid')
			  statusValue = request.form.get('status')
			  print(statusValue)
			  if statusValue == 'put':
				  cursor.execute("UPDATE contact SET status = %s WHERE contact.contactid = %s",
				  (True,contactid,))
			  else:
				  cursor.execute("DELETE FROM contact WHERE contactid=%s" , (str(contactid),))

			  conn.commit()
			  conn.close()
			  return redirect(url_for('all_contacts', status="done" ))
		  else:
			  if "authority" in session:
				  authority = session['authority']
				  cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username FROM members 
								    INNER JOIN personaldata 
								    ON personaldata.memberid = members.memberid and members.memberid = %s """,
							     (str(session["id"]),))
				  data = cursor.fetchall()

				  if authority == 'admin':
					  cursor.execute("SELECT contactid, message, date, title, category, e_mail, status FROM contact")
					  contacts = cursor.fetchall()

				  if contacts:
					  conn.close()
					  return render_template("show-contacts.html",authority=session["authority"] , contact=contacts, datam=data, contactlen=len(contacts))
				  else:
					  conn.close()
					  return render_template("show-contacts.html",authority=session["authority"] ,  datam=data, contactlen=0, result="No contact..")
			  else :
				  conn.close()
				  return render_template(url_for("profile"))

   In this method, if the logged-in users authority is admin, a button opens to display the 'contacts' and the admin can view the problems such as suggestions, complaints. Admin can delete or mark these comments as seen.

   .. code-block:: python

      @app.route('/sign-in', methods=['GET'])
	  def get_members():
		  conn = dpapi.connect(url)
		  cursor = conn.cursor()
		  userName = request.args.get("username")
		  passWord = request.args.get("password")

		  if userName and passWord:
			  print(hashlib.md5(passWord.encode('utf-8')).hexdigest())
			  if request.form.get("forgotPassword"):
			  	  return render_template("index.html")
			  cursor.execute("SELECT * FROM members where username=%s and userpassword=%s",(userName,hashlib.md5(passWord.encode('utf-8')).hexdigest()))
			  data = cursor.fetchone()
			  conn.commit()
			  if data:
				  session["username"]= userName
				  session["id"] = data[0]
				  session['authority'] = data[6]
				  conn.close()
				  return redirect(url_for('home', username=session["username"]))
			  else:
			  	  myerror="Please try again!"
				  conn.close()
				  return render_template('login-page.html', errors=myerror)
		  else :
			  conn.close()
			  return render_template("login-page.html")


   This method allows the user to login if the username and password entered in the are correct in the database, redirects to the home page, if wrong, gives an error message.

   .. code-block:: python

      @app.route('/logout', methods=['GET'])
	  def logout():
	     conn = dpapi.connect(url)
	     cursor = conn.cursor()

	     if 'id' in session:
			  session.pop('id')
	     if 'username' in session:
			  session.pop('username')

	     conn.close()
	     return redirect(url_for('home'))

   This method allows the user to log out. The username and id popped from session to log out.

   .. code-block:: python

      @app.route('/sign-up', methods=['GET','POST'])
	  def signUp():
		  conn = dpapi.connect(url)
		  cursor = conn.cursor()
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
				  cursor.execute("INSERT INTO members(username, userpassword, e_mail, recoveryques, recoveryans, authority) VALUES (%s, %s, %s, %s, %s, %s) RETURNING memberid",(username, hashlib.md5(password.encode('utf-8')).hexdigest(), email, rques, ranswer, 'user'))
				  conn.commit()
				  sql=cursor.fetchone()[0]
				  cursor.execute("INSERT INTO personaldata (name, surname, birthdate, sex, location, memberid) "
								   "VALUES (%s,%s,%s,%s,%s,%s)", (firstname, lastname, birthdate, gender, location, sql))
				  conn.commit()

				  session["username"] = username
				  session["id"] = sql
				  session['authority'] = 'user'
				  conn.close()
				  return redirect(url_for('home', username=session["username"]))
			
		  elif request.method == 'GET':
			  conn.close()
			  return render_template("sign-page.html")

   This method receives the necessary information from the user and performs the membership process. User must enter all information to become a member. Redirects to the home page after becoming a member.

   .. code-block:: python

      @app.route('/add-recipe', methods=['GET','POST'])
	  def post_food():
      conn = dpapi.connect(url)
      cursor = conn.cursor()
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
                  print("food", id)
                  conn.commit()
              elif recipeType == "beverage":
                  cursor.execute(
                      "INSERT INTO beverage(beveragename, beveragerecipe, beveragephoto, beveragetype, qualificationid, memberid, beveragedate) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING beverageid",
                      (name, recipe, photo, type, qualificationId, memberid, date))
                  id = cursor.fetchone()[0]
                  print("beverage", id)
                  conn.commit()
              elif recipeType == "dessert":
                  cursor.execute(
                      "INSERT INTO dessert(dessertname, dessertrecipe, dessertphoto, desserttype, qualificationid, memberid, dessertdate) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING dessertid",
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

              cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username FROM members 
                                         INNER JOIN personaldata 
                                         ON personaldata.memberid = members.memberid and members.memberid = %s """,
                             (session["id"],))
              data2 = cursor.fetchall()
              conn.close()
              return redirect(url_for("profile"))
      else:
          if "id" in session:
              print(session["id"])
              cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username FROM members 
                              INNER JOIN personaldata 
                              ON personaldata.memberid = members.memberid and members.memberid = %s """,(session["id"],))
              data = cursor.fetchall()
          conn.close()

   In this method, the user first selects whether the recipe he wants to add is food or dessert. Then uploads the recipe by adding all the necessary ingredients, recipe, informations and photo. The user has to enter them all.

   .. code-block:: python

      @app.route('/change-recipe/food/<id>', methods=['GET','POST'])
	  def change_food(id):
		  conn = dpapi.connect(url)
		  cursor = conn.cursor()
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
			  conn.close()
			  return redirect(url_for("profile"))
		  else:
			  mymemberid = session["id"]
			  cursor.execute(""" SELECT food.foodname, qualification.cuisine, qualification.calori, qualification.serve,  qualification.timing, qualification.category,food.foodrecipe, food.foodtype, qualification.qualificationid FROM qualification
						  INNER JOIN food
						  ON food.qualificationid = qualification.qualificationid and food.foodid=%s""", (id,))
			  foods = cursor.fetchone()
			  print(foods[4])
			  cursor.execute("SELECT ingredient.ingrename, ingredient.unit, ingredient.amount, ingredient.ingredientid FROM ingredient INNER JOIN food ON ingredient.foodid = food.foodid AND food.foodid = %s """,(id,))
			  data3 = cursor.fetchall()
			  print(data3)
			  cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username FROM members 
								 INNER JOIN personaldata 
								 ON personaldata.memberid = members.memberid and members.memberid = %s """,(mymemberid,))
			  memberdata = cursor.fetchall()
			  conn.close()
			  return render_template("change-recipe.html",  authority=session["authority"]  ,datam=memberdata, data=foods , ingre=data3 , ingrelen=len(data3))


   In this method, the name of the food, the recipe, the ingredient name and amount, and the qualification properties of the food can be changed. So update operation is made.

   .. code-block:: python

      @app.route('/change-recipe/dessert/<id>', methods=['GET','POST'])
	  def change_dessert(id):
		  conn = dpapi.connect(url)
		  cursor = conn.cursor()
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
			  conn.close()
			  return redirect(url_for("profile"))
		  else:
			  cursor.execute(""" SELECT dessert.dessertname, qualification.cuisine, qualification.calori, qualification.serve,  qualification.timing, qualification.category,dessert.dessertrecipe, dessert.desserttype, qualification.qualificationid FROM qualification
						  INNER JOIN dessert
						  ON dessert.qualificationid = qualification.qualificationid and dessert.dessertid=%s""", (id,))
			  desserts = cursor.fetchone()
			  cursor.execute("SELECT ingredient.ingrename, ingredient.unit, ingredient.amount, ingredient.ingredientid FROM ingredient INNER JOIN dessert ON ingredient.dessertid = dessert.dessertid AND dessert.dessertid = %s """,(id,))
			  data3 = cursor.fetchall()
			  print(data3)
			  cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username FROM members 
							     INNER JOIN personaldata 
							     ON personaldata.memberid = members.memberid and members.memberid = %s """,
						     (str(session["id"]),))
			  memberdata = cursor.fetchall()
			  conn.close()
			  return render_template("change-recipe.html",  authority=session["authority"] , datam=memberdata, data=desserts , ingre=data3 , ingrelen=len(data3))


   In this method, the name of the dessert, the recipe, the ingredient name and amount, and the qualification properties of the dessert can be changed. So update operation is made.


   .. code-block:: python
   
      @app.route('/change-recipe/drink/<id>', methods=['GET','POST'])
	  def change_drink(id):
		  conn = dpapi.connect(url)
		  cursor = conn.cursor()
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
			  conn.close()
			  return redirect(url_for("profile"))
		  else:
		  	  cursor.execute(""" SELECT beverage.beveragename, qualification.cuisine, qualification.calori, qualification.serve,  qualification.timing, qualification.category,beverage.beveragerecipe, beverage.beveragetype, qualification.qualificationid FROM qualification
						  INNER JOIN beverage
						  ON beverage.qualificationid = qualification.qualificationid and beverage.beverageid=%s""", (id,))
			  drinks= cursor.fetchone()

			  cursor.execute("SELECT ingredient.ingrename, ingredient.unit, ingredient.amount, ingredient.ingredientid FROM ingredient INNER JOIN beverage ON ingredient.beverageid = beverage.beverageid AND beverage.beverageid = %s """,(id,))
			  data3 = cursor.fetchall()
			  print(data3)
			  cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username FROM members 
							     INNER JOIN personaldata 
							     ON personaldata.memberid = members.memberid and members.memberid = %s """,
						     (str(session["id"]),))
			  memberdata = cursor.fetchall()
			  conn.close()
			  return render_template("change-recipe.html",  authority=session["authority"] , datam=memberdata, data=drinks , ingre=data3 , ingrelen=len(data3))



   In this method, the name of the beverage, the recipe, the ingredient name and amount, and the qualification properties of the beverage can be changed. So update operation is made.

   .. code-block:: python

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


   This method allows to upload photo to recipes.

  
