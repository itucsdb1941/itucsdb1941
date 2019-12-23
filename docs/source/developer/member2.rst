Parts Implemented by Ilgin Balkan
================================




**explain the technical structure of your code**

**to include a code listing, use the following example**:

  
   .. code-block:: python

	  @app.route('/profile', methods=['GET' , 'POST'])
	  def profile():
		  conn = dpapi.connect(url)
		  cursor = conn.cursor()
		  if "id" in session:
			  cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username, personaldata.personalid FROM members 
						     INNER JOIN personaldata 
						     ON personaldata.memberid = members.memberid and members.memberid=%s;""", (session["id"],))
			  data = cursor.fetchall()

			  cursor.execute(""" SELECT food.foodid, food.foodphoto, food.foodname, qualification.cuisine, qualification.timing, qualification.qualificationid, food.foodrecipe FROM qualification
						  INNER JOIN food
						  ON food.qualificationid = qualification.qualificationid and food.memberid = %s;""",(session["id"],))

			  foods = cursor.fetchall()

			  cursor.execute(""" SELECT dessert.dessertid, dessert.dessertphoto, dessert.dessertname, qualification.cuisine, qualification.timing, qualification.qualificationid, dessert.dessertrecipe FROM qualification
							  INNER JOIN dessert
							  ON dessert.qualificationid = qualification.qualificationid and dessert.memberid = %s;""",(session["id"],))

			  desserts = cursor.fetchall()

			  cursor.execute(""" SELECT beverage.beverageid, beverage.beveragephoto, beverage.beveragename, qualification.cuisine, qualification.timing, qualification.qualificationid, beverage.beveragerecipe FROM qualification
						  	  INNER JOIN beverage
							  ON beverage.qualificationid = qualification.qualificationid and beverage.memberid = %s;""", (session["id"],))

			  drinks = cursor.fetchall()

			  if request.method == 'POST':

				  deletedrink = request.form.get('drinkdelete')
				  deletedessert = request.form.get('dessertdelete')
				  deletefood = request.form.get('fooddelete')

				  if deletedrink:
					  i = 0

					  while i < len(drinks):
						  deletedrink = drinks[i][0]
						  qid = drinks[i][5]
						  cursor.execute(""" DELETE FROM comment WHERE comment.beverageid=%s""", (str(deletedrink),))
						  cursor.execute( """ DELETE FROM ingredient WHERE ingredient.beverageid IN (SELECT beverageid FROM beverage WHERE beverage.beverageid = %s)""", (str(deletedrink),))
						  cursor.execute(""" DELETE FROM beverage WHERE beverage.beverageid= %s""", (str(deletedrink),))
						  cursor.execute(""" DELETE FROM qualification WHERE qualification.qualificationid=%s """,
									     (str(qid),))
						  conn.commit()
						  i = i + 1
					  conn.close()
					  return redirect(url_for('profile'))

				  elif deletefood:
					  i = 0

					  while i < len(foods):
						  deletefood = foods[i][0]
						  qid = foods[i][5]
						  cursor.execute(""" DELETE FROM comment WHERE comment.foodid=%s""", (str(deletefood),))
						  cursor.execute( """ DELETE FROM ingredient WHERE ingredient.foodid IN (SELECT foodid FROM food WHERE food.foodid = %s)""",  (str(deletefood),))
						  cursor.execute(""" DELETE FROM food WHERE food.foodid= %s""", (str(deletefood),))
						  cursor.execute(""" DELETE FROM qualification WHERE qualification.qualificationid=%s """,
									     (str(qid),))
						  conn.commit()
						  i = i + 1
					  conn.close()
					  return redirect(url_for('profile'))

				  elif deletedessert:
					  i = 0

					  while i < len(desserts):

						  deletedessert = desserts[i][0]
						  print(desserts[i][0])

						  qid = desserts[i][5]
						  cursor.execute(""" DELETE FROM comment WHERE comment.dessertid=%s""",  (str(deletedessert),))
						  cursor.execute( """ DELETE FROM ingredient WHERE ingredient.dessertid IN (SELECT dessertid FROM dessert WHERE dessert.dessertid = %s)""", (str(deletedessert),))
					  	  cursor.execute(""" DELETE FROM dessert WHERE dessert.dessertid= %s""", (str(deletedessert),))
						  cursor.execute(""" DELETE FROM qualification WHERE qualification.qualificationid=%s """, (str(qid),))
						  conn.commit()
						  i = i + 1
					  conn.close()
					  return redirect(url_for('profile'))

			  if data or foods or drinks or desserts:
				  conn.close()
				  return render_template("profile.html", authority=session["authority"] , datam=data, foodlen =len(foods), drinklen =len(drinks), dessertlen=len(desserts), food=foods, dessert=desserts, drink=drinks)
			  else:
				  conn.close()
				  return render_template("profile.html" , datam=data, authority=session["authority"]  ,foodlen =len(foods),drinklen =len(drinks), dessertlen=len(desserts), food=foods, dessert=desserts, drink=drinks)

		  conn.close()
		  return render_template("index.html")

   In this method, first of all, the user's personal data and if added, the food, dessert and beverage recipes appear on the profile screen as cards. By pressing the delete button on these cards, POST method is performed and comments, qualification and ingredients related to that recipe are deleted according to the type(food, beverage or dessert) of recipe.

   .. code-block:: python

      @app.route('/change-info', methods=['GET' , 'POST'])
	  def changeInfo():
		  conn = dpapi.connect(url)
		  cursor = conn.cursor()
		  firstname = request.form.get("FirstName")
		  lastname = request.form.get("LastName")
		  gender = request.form.get("Gender")
		  birthdate = request.form.get("Birthdate")
		  location = request.form.get("Location")
	  	  email = request.form.get("email")
		  password = request.form.get("password")

		  cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.location, members.e_mail, members.username,  members.userpassword FROM members 
										  INNER JOIN personaldata 
										  ON personaldata.memberid = members.memberid and members.memberid = %s """, (str(session["id"]),))
		  data2 = cursor.fetchall()
		  print(data2)

		  if request.method == "POST":
			  cursor.execute(
				  "UPDATE personaldata SET name = %s, surname = %s , birthdate = %s, sex = %s, location = %s  WHERE personaldata.memberid = %s",
				  (firstname, lastname, birthdate, gender, location, session["id"]))
			  cursor.execute(
				  "UPDATE members SET e_mail = %s, userpassword = %s WHERE members.memberid = %s",
				  (email, hashlib.md5(password.encode('utf-8')).hexdigest(), session["id"]))
			  conn.commit()
			  conn.close()
			  return redirect(url_for('profile', authority=session["authority"] , datam=data2))

		  else:
			  cursor.execute("""SELECT members.memberid, personaldata.name, personaldata.surname, personaldata.sex, personaldata.birthdate, personaldata.location, members.userpassword FROM personaldata 
								  INNER JOIN members 
								  ON personaldata.memberid = members.memberid and members.memberid = %s """,(str(session["id"]),))
			  data = cursor.fetchall()
			  print(data)
			  conn.close()
			  return render_template('change-info.html',  authority=session["authority"] , info=data, datam=data2)


   In this method allows the user to modify his/her personal data.

   .. code-block:: python

      @app.route('/new-password', methods=['GET'])
	  def newPass():
		  conn = dpapi.connect(url)
		  cursor = conn.cursor()
		  userName = request.args.get("username")
		  e_mail = request.args.get("email")
		  answer = request.args.get("answer")
		  newpassword = request.args.get("password")


		  cursor.execute("SELECT recoveryques, recoveryans, memberid FROM members where username=%s and e_mail=%s",(userName,e_mail))
		  data = cursor.fetchone()


		  if data:
		  	  session['memberid'] = data[2]
			  print(data[2])
			  conn.close()
			  return render_template('new-password.html', email=e_mail, datam=data)

		  if answer:
			  data = 'a'
			  memberid = session['memberid']
			  print("aa",memberid)
			  conn.close()
			  return render_template('new-password.html', datam=data, ans=answer, memberid=memberid)

		  if newpassword:
			  memberid = session['memberid']
			  print("bb",memberid)
			  cursor.execute("UPDATE members SET userpassword = %s  WHERE members.memberid = %s", (hashlib.md5(newpassword.encode('utf-8')).hexdigest(), memberid))
			  conn.commit()
			  conn.close()
			  return redirect(url_for('profile', id=id))
			  
		  conn.close()
		  return render_template('new-password.html')

   In this method, if the user has forgotten his password, he/she enters his email and username. According to this information, the user's recovery question comes from the database, if the user enters the correct answer, he/she can change the password and be directed to the home page.

   .. code-block:: python

      @app.route('/food-menu', methods=['GET'])
	  def foods():
		  conn = dpapi.connect(url)
		  cursor = conn.cursor()
		  cursor.execute("""
				  	  SELECT food.foodid, food.foodphoto, food.foodname, qualification.cuisine, qualification.timing, qualification.qualificationid  FROM qualification
					  INNER JOIN food
					  ON food.qualificationid = qualification.qualificationid""")

		  data = cursor.fetchall()
		  username = ""
		  if 'username' in session:
			  username = session['username']
		  if data:
			  conn.close()
			  return render_template("food-menu.html", len = len(data), food=data, username=username)
		  else:
			   conn.close()
			  return render_template("food-menu.html", username=username)

   In this method, all the foods added up to now appear in cards, and when any of them is clicked, it directs to the recipe.

   .. code-block:: python

      @app.route('/drink-menu', methods=['GET'])
	  def drinks():
	  	  conn = dpapi.connect(url)
		  cursor = conn.cursor()
		  cursor.execute("""
					  SELECT beverage.beverageid, beverage.beveragephoto, beverage.beveragename,  qualification.cuisine,  qualification.timing, qualification.qualificationid FROM qualification
					  INNER JOIN beverage
					  ON beverage.qualificationid = qualification.qualificationid""")

		  data = cursor.fetchall()
		  username = ""
		  if 'username' in session:
			  username = session['username']
		  if data:
			  conn.close()
			  return render_template("drink-menu.html", len=len(data), drink=data, username=username)
		  else:
			  conn.close()
			  return render_template("drink-menu.html", username=username)
	  
	  
   In this method, all the beverages added up to now appear in cards, and when any of them is clicked, it directs to the recipe.

   .. code-block:: python

      @app.route('/dessert-menu', methods=['GET'])
	  def desserts():
		  conn = dpapi.connect(url)
		  cursor = conn.cursor()
		  cursor.execute("""
					  SELECT dessert.dessertid,  dessert.dessertphoto, dessert.dessertname, qualification.cuisine, qualification.timing, qualification.qualificationid FROM qualification
					  INNER JOIN dessert
					  ON dessert.qualificationid = qualification.qualificationid""")

		  data = cursor.fetchall()
		  username = ""
		  if 'username' in session:
			 username = session['username']
		  if data:
			  conn.close()
			  return render_template("dessert-menu.html", len=len(data), dessert=data, username=username)
		  else:
			  conn.close()
			  return render_template("dessert-menu.html", username=username)


   In this method, all the desserts added up to now appear in cards, and when any of them is clicked, it directs to the recipe.

   .. code-block:: python

      @app.route('/recipe/food/<id>', methods=['GET', 'POST'])
	  def foodRecipe(id):

		  conn = dpapi.connect(url)
		  cursor = conn.cursor()
		  if request.method == 'POST':
		  	  mytitle = request.form.get("title")
			  mycomment = request.form.get("comment")
			  like = request.form.get("like")
			  dislike = request.form.get("dislike")
			  comment_id = request.form.get("commentid")
			  date = request.form.get("commentdate")

			  print(comment_id)
			  if like == "PUT":
			  	  cursor.execute("UPDATE comment SET commentlike = commentlike + 1 WHERE comment.foodid = %s and comment.commentid = %s ", (id,comment_id))
				  conn.commit()
				  conn.close()
				  return redirect(url_for('foodRecipe', id=id))

			  elif dislike == "PUT":
				  cursor.execute("UPDATE comment SET commentdislike = commentdislike + 1 WHERE comment.foodid = %s and comment.commentid = %s ", (id,comment_id))
				  conn.commit()
				  conn.close()
				  return redirect(url_for('foodRecipe', id=id))

			  if mycomment and mytitle:
				  cursor.execute("INSERT INTO comment(usercomment, title, foodid, memberid, commentdate) VALUES (%s, %s, %s, %s, %s)",
							     (mycomment, mytitle, id, str(session["id"]), date))
				  conn.commit()
				  conn.close()
				  return redirect(url_for('foodRecipe', id=id))
		  else:
			  cursor.execute("""
						  SELECT food.foodid, food.foodname, food.foodphoto, food.foodrecipe, ingredient.ingrename, ingredient.unit, ingredient.amount, qualification.cuisine, qualification.qualificationid, qualification.timing, food.fooddate, qualification.calori, qualification.serve, qualification.category, food.memberid, food.foodtype FROM food
						  INNER JOIN qualification
						  ON food.qualificationid = qualification.qualificationid
						  INNER JOIN  ingredient
						  ON ingredient.foodid = food.foodid AND food.foodid = %s""", (id,))
			  data = cursor.fetchone()
			  foodid = data[0]
			  memberid=data[14]
			  cursor.execute("SELECT comment.usercomment, comment.commentdate, members.username, comment.title, comment.commentlike, comment.commentdislike, comment.commentid FROM comment INNER JOIN members ON comment.memberid = members.memberid where comment.foodid = %s ", (foodid,))
			  data2 = cursor.fetchall()

			  cursor.execute("SELECT ingredient.ingrename, ingredient.unit, ingredient.amount, ingredient.allergenic FROM ingredient INNER JOIN food ON ingredient.foodid = food.foodid AND food.foodid = %s """,(id,))
			  data3 = cursor.fetchall()

			  cursor.execute("SELECT username FROM members where memberid=%s",(memberid,))
			  foodusername = cursor.fetchone()
			  username = ""
			  if 'username' in session:
				  username = session['username']
			  if data:
				  conn.close()
				  return render_template("recipe.html", len=len(data2), len2=len(data3), datam=data , fooduser=foodusername ,comment=data2, ingre=data3, username=username)

		  conn.close()
		  return render_template("recipe.html")



    In this method, the user can access the recipe, the photograph, the ingredients of the food. In addition, user can see foods' cuisine, cooking time, type, calorie amount, serving amount. If the user has logged in, he/she can comment on the food and give like or dislike.


   .. code-block:: python
   
      @app.route('/recipe/drink/<id>', methods=['GET', 'POST'])
	  def drinkRecipe(id):
		  conn = dpapi.connect(url)
		  cursor = conn.cursor()

		  if request.method == 'POST':
			  mytitle = request.form.get("title")
			  mycomment = request.form.get("comment")
			  like = request.form.get("like")
			  dislike = request.form.get("dislike")
			  comment_id = request.form.get("commentid")
			  date = request.form.get("commentdate")

			  print(comment_id)
			  if like == "PUT":
				  cursor.execute(
					  "UPDATE comment SET commentlike = commentlike + 1 WHERE comment.beverageid = %s and comment.commentid = %s ",
					  (id, comment_id))
				  conn.commit()
				  conn.close()
				  return redirect(url_for('drinkRecipe', id=id))

			  elif dislike == "PUT":
				  cursor.execute(
					  "UPDATE comment SET commentdislike = commentdislike + 1 WHERE comment.beverageid = %s and comment.commentid = %s ",
					  (id, comment_id))
				  conn.commit()
				  conn.close()
				  return redirect(url_for('drinkRecipe', id=id))

			  if mycomment and mytitle:
				  cursor.execute("INSERT INTO comment(usercomment, title, beverageid, memberid, commentdate) VALUES (%s, %s, %s, %s, %s)",
							     (mycomment, mytitle, id,  str(session["id"]), date))
				  conn.commit()
				  conn.close()
				  return redirect(url_for('drinkRecipe', id=id))
		  else:
			  cursor.execute("""
								  SELECT beverage.beverageid, beverage.beveragename, beverage.beveragephoto, beverage.beveragerecipe, ingredient.ingrename, ingredient.unit, ingredient.amount, qualification.cuisine, qualification.qualificationid, qualification.timing, beverage.beveragedate, qualification.calori, qualification.serve, qualification.category, beverage.memberid, beverage.beveragetype FROM beverage
								  INNER JOIN qualification
								  ON beverage.qualificationid = qualification.qualificationid
								  INNER JOIN  ingredient
								  ON ingredient.beverageid = beverage.beverageid AND beverage.beverageid = %s""", (id,))
			  data = cursor.fetchone()
			  drinkid = data[0]
			  memberid = data[14]
			  cursor.execute(
				  "SELECT comment.usercomment, comment.commentdate, members.username, comment.title, comment.commentlike, comment.commentdislike, comment.commentid  FROM comment INNER JOIN members ON comment.memberid = members.memberid where comment.beverageid = %s ",
				  (drinkid,))
			  data2 = cursor.fetchall()

			  cursor.execute(
				  "SELECT ingredient.ingrename, ingredient.unit, ingredient.amount, ingredient.allergenic FROM ingredient INNER JOIN beverage ON ingredient.beverageid = beverage.beverageid AND beverage.beverageid = %s """,
				  (id,))
			  data3 = cursor.fetchall()

			  cursor.execute("SELECT username FROM members where memberid=%s", (memberid,))
			  beverageuser = cursor.fetchone()

			  username = ""
			  if 'username' in session:
				  username = session['username']

			  if data:
				  conn.close()
				  return render_template("recipe.html", len=len(data2), len2=len(data3), datam=data, fooduser=beverageuser ,comment=data2, ingre=data3, username=username)

		  conn.close()
		  return render_template("recipe.html")



    In this method, the user can access the recipe, the photograph, the ingredients of the beverage. In addition, user can see beverages' cuisine, cooking time, type, calorie amount, serving amount. If the user has logged in, he/she can comment on the beverage and give like or dislike.

   .. code-block:: python

      @app.route('/recipe/dessert/<id>', methods=['GET', 'POST'])
	  def dessertRecipe(id):
		  conn = dpapi.connect(url)
		  cursor = conn.cursor()
		  print(session)
		  if request.method == 'POST':
			  mytitle = request.form.get("title")
			  mycomment = request.form.get("comment")
			  like = request.form.get("like")
			  dislike = request.form.get("dislike")
			  comment_id = request.form.get("commentid")
			  date = request.form.get("commentdate")
			  print(date)

			  if like == "PUT":
			   	  cursor.execute(
					  "UPDATE comment SET commentlike = commentlike + 1 WHERE comment.dessertid = %s and comment.commentid = %s ",
					  (id, comment_id))
				  conn.commit()
				  conn.close()
				  return redirect(url_for('dessertRecipe', id=id))

			  elif dislike == "PUT":
				  cursor.execute(
					  "UPDATE comment SET commentdislike = commentdislike + 1 WHERE comment.dessertid = %s and comment.commentid = %s ",
					  (id, comment_id))
				  conn.commit()
				  conn.close()
				  return redirect(url_for('dessertRecipe', id=id))

			  if mycomment and mytitle:
				  cursor.execute("INSERT INTO comment(usercomment, title, dessertid, memberid, commentdate) VALUES (%s, %s, %s, %s, %s)",
							     (mycomment, mytitle, id,  str(session["id"]), date))
				  conn.commit()
				  conn.close()
				  return redirect(url_for('dessertRecipe', id=id))
		  else:
			  cursor.execute("""
			 					  SELECT dessert.dessertid, dessert.dessertname, dessert.dessertphoto, dessert.dessertrecipe, ingredient.ingrename, ingredient.unit, ingredient.amount, qualification.cuisine, qualification.qualificationid, qualification.timing, dessert.dessertdate, qualification.calori, qualification.serve, qualification.category, dessert.memberid, dessert.desserttype FROM dessert
								  INNER JOIN qualification
								  ON dessert.qualificationid = qualification.qualificationid
								  INNER JOIN  ingredient
								  ON dessert.dessertid = dessert.dessertid AND dessert.dessertid = %s""", (id,))
			  data = cursor.fetchone()
			  dessertid = data[0]
			  memberid = data[14]
			  cursor.execute(
				  "SELECT comment.usercomment, comment.commentdate, members.username, comment.title, comment.commentlike, comment.commentdislike, comment.commentid FROM comment INNER JOIN members ON comment.memberid = members.memberid where comment.dessertid = %s ",
				  (dessertid,))
			  data2 = cursor.fetchall()

			  cursor.execute(
				  "SELECT ingredient.ingrename, ingredient.unit, ingredient.amount, ingredient.allergenic FROM ingredient INNER JOIN dessert ON ingredient.dessertid = dessert.dessertid AND dessert.dessertid = %s """,
				  (id,))
			  data3 = cursor.fetchall()

			  cursor.execute("SELECT username FROM members where memberid=%s", (memberid,))
			  dessertuser = cursor.fetchone()

			  username = ""
			  if 'username' in session:
				  username = session['username']
			  if data:
				  conn.close()
				  return render_template("recipe.html", len=len(data2), len2=len(data3), datam=data, fooduser=dessertuser ,comment=data2, ingre=data3, username=username)

		  conn.close()
		  return render_template("recipe.html")


    In this method, the user can access the recipe, the photograph, the ingredients of the dessert. In addition, user can see desserts' cuisine, cooking time, type, calorie amount, serving amount. If the user has logged in, he/she can comment on the dessert and give like or dislike.

  
   .. code-block:: python

      @app.route('/contact', methods=['GET', 'POST'])
	  def contact():
		  conn = dpapi.connect(url)
		  cursor = conn.cursor()
		  if request.method == 'POST':

			  username = ""
			  if 'username' in session:
				  username = session['username']

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
				  conn.close()
				  return redirect(url_for('home'))

			  else:
				  conn.close()
				  return render_template("contact.html", username=username)
		  else:
			  username = ""
			  if 'username' in session:
				  username = session['username']
			  conn.close()
			  return render_template("contact.html", username=username)


   In this method, users can write message about complaints, suggestions or recipes related to the site. Only admins can view. Does not require user login to send messages.	
