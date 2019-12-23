Parts Implemented by Simge Tiraş
================================




**explain the technical structure of your code**

**to include a code listing, use the following example**:

  
   .. code-block:: python

      
	  @app.route('/', methods=['GET'])
	  def home():
		  conn = dpapi.connect(url)
		  cursor = conn.cursor()
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
								  ORDER BY food.fooddate DESC NULLS LAST """)
		  data4 = cursor.fetchone()

		  cursor.execute("""SELECT  dessert.dessertid, dessert.dessertname, dessert.dessertrecipe, dessert.dessertphoto, dessert.dessertdate FROM dessert 
									  ORDER BY dessert.dessertdate DESC NULLS LAST """)
		  data5 = cursor.fetchone()

		  cursor.execute("""SELECT  beverage.beverageid, beverage.beveragename, beverage.beveragerecipe, beverage.beveragephoto, beverage.beveragedate FROM beverage 
									  ORDER BY beverage.beveragedate DESC NULLS LAST """)
		  data6 = cursor.fetchone()

	     # cursor.execute("SELECT food.foodid, food.foodname, food.foodrecipe, food.foodphoto, food.foodtype, food.foodscore FROM food ORDER BY foodscore ASC LIMIT 1")
	     # data2 = cursor.fetchall()

		  username = ""
		  if 'username' in session:
			  username = session['username']

		  if data or data2 or data3 or data4 or data5 or data6:
			  conn.close()
			  return render_template("index.html", comment1 =data, len=len(data), comment2=data2, comment3=data3, beverage=data6, food= data4, dessert= data5, username=username)
		  else:
			  conn.close()
			  return render_template("index.html", username=username)


   At the bottom of the main page of the project shows the most recently added recipes and the most like comments. Therefore, in this section, we have listed the comments in the database according to the likes of the comments and showed the most liked comments. At the same time, while adding food, drinks and desserts, according to the recipe dates, we took the most recently added dishes from the database with the Select command and showed them on the home page.
	 

   .. code-block:: python

      else:
		  i=0
		  while i < len(foods):
			  foodid = foods[i][0]
			  qid = foods[i][5]
			  print(qid, str(foodid))
			  cursor.execute(""" DELETE FROM comment WHERE comment.memberid=%s""", (str(session["id"]),))
			  cursor.execute(""" DELETE FROM ingredient WHERE ingredient.foodid IN (SELECT foodid FROM food WHERE food.memberid = %s)""", (str(session["id"]),))
			  cursor.execute(""" DELETE FROM food WHERE food.foodid= %s""", (str(foodid),))
			  cursor.execute(""" DELETE FROM qualification WHERE qualification.qualificationid=%s """, (str(qid),))
			  conn.commit()
			  i = i + 1

		  i = 0
          while i < len(drinks):
			  drinkid = drinks[i][0]
			  qid = drinks[i][5]
			  cursor.execute(""" DELETE FROM comment WHERE comment.memberid=%s""", (str(session["id"]),))
			  cursor.execute(""" DELETE FROM ingredient WHERE ingredient.beverageid IN (SELECT beverageid FROM beverage WHERE beverage.memberid = %s)""",(str(session["id"]),))
			  cursor.execute(""" DELETE FROM beverage WHERE beverage.beverageid= %s""", (str(drinkid),))
			  cursor.execute(""" DELETE FROM qualification WHERE qualification.qualificationid=%s """, (str(qid),))
			  conn.commit()
              i = i + 1

          i = 0
          while i < len(desserts):
			  dessertid = desserts[i][0]
              qid = desserts[i][5]
              cursor.execute(""" DELETE FROM comment WHERE comment.memberid= %s""", (str(session["id"]),))
              cursor.execute(""" DELETE FROM ingredient WHERE ingredient.dessertid IN (SELECT dessertid FROM dessert WHERE dessert.memberid = %s)""",(str(session["id"]),))
		      cursor.execute(""" DELETE FROM dessert WHERE dessert.dessertid= %s""", (str(dessertid),))
              cursor.execute(""" DELETE FROM qualification WHERE qualification.qualificationid=%s """, (str(qid),))
              conn.commit()
              i = i + 1


          cursor.execute(""" DELETE FROM personaldata WHERE memberid= %s""", (str(session["id"]),))
          cursor.execute(""" DELETE FROM members WHERE memberid= %s""", (str(session["id"]),))
          conn.commit()

          if 'id' in session:
              session.pop('id')
          if 'username' in session:
              session.pop('username')

          conn.close()
          return redirect(url_for('home'))


   If the user presses delete my account in the profile, all recipes, comments and personal information about that user is deleted.
