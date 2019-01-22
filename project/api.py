# -*- coding: utf-8 -*-
import json
import mysql.connector
import pymysql.cursors
from project.views import jsonApi
import datetime

GLOBAL_RESULTS_LIMIT = 100
GLOBAL_CALC_RESULTS_LIMITS = 10000

####################################################################
####	Functions:						####
####################################################################
# 1)  def getCursor():						####
# 2)  def apiShowTables():					####
# 3)  def apiSuggestion(request):				####
# 4)  def cursorToJSON(cursor):					####
# 5)  def apiRecipeByNumOfIngredients(num):			####
# 6)  def apiRecipeByMaxPrepTime(time):				####
# 7)  def apiRecipeByDiet(diet):				####
# 8)  def apiRecipeByCategory(category):			####
# 9)  def apiRecipeByDishName(name):				####
# 10) def apiMealByNumRecipiesAndTotalTime(numRecipies, time):	####
# 11) def apiOneMealByTotalTime(time):				####
# 12) def apiTwoMealsByTotalTime(time):				####
# 13) def apiThreeMealsByTotalTime(time):			####
# 14) def apiFourMealsByTotalTime(time):			####
# 15) def apiFiveMealsByTotalTime(time):			####
# 16) def apiRecipeByIngredientList(list):			####
# 17) def apiRecipeByOneIngredient(list):			####
# 18) def apiRecipeByTwoIngredients(list):			####
# 19) def apiRecipeByThreeIngredients(list):			####
# 20) def apiRecipeByFourIngredients(list):			####
# 21) def apiRecipeByFiveIngredients(list):			####
####################################################################
def getCursor():
	connection = pymysql.connect(host='localhost',
					port=3305,
					user='DbMysql14',
					password='DbMysql14',
					db='DbMysql14',
					charset='utf8mb4',
					cursorclass=pymysql.cursors.DictCursor)
	# connection = pymysql.connect(host='delta-tomcat-vm.cs.tau.ac.il',
	# 				port=40777,
	# 				user='DbMysql14',
	# 				password='DbMysql14',
	# 				db='DbMysql14',
	# 				cursorclass=pymysql.cursors.DictCursor)
	return connection.cursor()

def apiShowTables():
	cursor = getCursor()
	cursor.execute("show tables")
	for row in cursor:
		print(row)

def apiSuggestion(request):
	if not request.is_ajax():
		return jsonApi(300, "Invalid call")
	# res = apiRecipeByNumOfIngredients(2) -> Checked
	# res = apiRecipeByDiet('balanced') -> Checked
	# res = apiRecipeByIngredientList(["liqueur", "apple"]) -> Checked
	# res = apiRecipeByCategory('Meat') -> Checked
	# res = apiRecipeByDishName('Hot Apple Pie') -> Checked
	# res = apiRecipeByMaxPrepTime('00:04:00') -> Checked
	# res = apiMealByNumRecipiesAndTotalTime(1, '00:10:00') -> Checked
	# res = apiMealByNumRecipiesAndTotalTime(2, '00:10:00') -> Checked
	# res = apiMealByNumRecipiesAndTotalTime(3, '00:10:00') -> Checked
	# res = apiMealByNumRecipiesAndTotalTime(4, '00:10:00') -> Checked
	# res = apiMealByNumRecipiesAndTotalTime(5, '00:10:00') -> Checked
	#print(res) # XXX XXX XXX
	data = {"suggestions": [
			{ "value": "Arab Emirates", "data": "AE" },
			{ "value": "United Kingdom", "data": "UK" },
			{ "value": "United States", "data": "US" }
		]}
	return jsonApi(200, data)

def cursorToJSON(cursor):
	result = cursor.fetchall()
	for row in result:
		row['prep_time'] = str(row['prep_time'])
	data = {"results": len(result),
		"items": result}
	print("data:\n",data)
	return jsonApi(200, data)

def handler(o):
	if isinstance(o, (datetime.timedelta)):
		return str(o)

def apiDefaultResponse(request):
	if not request.is_ajax():
		return jsonApi(300, "Invalid call")
	data = {"results": 45321,
		"items": [
			{"id": 1, "name": "Balsamic-Glazed Steak Rolls", "prep_time": "02:15:00", "calories": 1999, "url": "https://Lorem.ipsum", "image": "https://images-gmi-pmc.edge-generalmills.com/7455fc0a-ffad-4526-8b68-e1a8b179914e.jpg"},
			{"id": 2, "name": "Mongolian Glazed Steak", "prep_time": "01:00:00", "calories": 2001, "url": "https://Lorem.at.ipsum", "image": "https://s3.amazonaws.com/supercook-thumbs/363402.jpg"},
			{"id": 3, "name": "Balsamic-Glazed Steak Rolls", "prep_time": "02:15:00", "calories": 1999, "url": "https://Lorem.ipsum", "image": "https://images-gmi-pmc.edge-generalmills.com/7455fc0a-ffad-4526-8b68-e1a8b179914e.jpg"},
			{"id": 4, "name": "Mongolian Glazed Steak", "prep_time": "01:00:00", "calories": 2001, "url": "https://Lorem.at.ipsum", "image": "https://s3.amazonaws.com/supercook-thumbs/363402.jpg"},
			{"id": 5, "name": "Balsamic-Glazed Steak Rolls", "prep_time": "02:15:00", "calories": 1999, "url": "https://Lorem.ipsum", "image": "https://images-gmi-pmc.edge-generalmills.com/7455fc0a-ffad-4526-8b68-e1a8b179914e.jpg"},
			{"id": 6, "name": "Mongolian Glazed Steak", "prep_time": "01:00:00", "calories": 2001, "url": "https://Lorem.at.ipsum", "image": "https://s3.amazonaws.com/supercook-thumbs/363402.jpg"}
		]}
	return jsonApi(200, data)

# Example for request:
# recipe_name=Hot+Apple+Pie&
# diet=any&
# prep_from=0&
# prep_to=180&
# ingredients_inc=&
# ingredients_exc=&
# sort_by=sort_by_name&
# sort_order=desc&
# page=0

# TODO: uncomment after UI implementation
# def apiIngredients(request):
# 	if not request.is_ajax():
# 		return jsonApi(300, "Invalid call")
# 	if ('selected_recipes' in request.GET):
# 		return apiIngredientsListByRecipiesList(request)

def apiRecipeByNumOfIngredients(request):
	num = request.GET['ingredients_max'].replace('+',' ') # 1 - To be implemented on UI
	cursor = getCursor()
	command = ("""
	SELECT rec_id AS id, rec_name AS name, Prep_Time AS prep_time, Calories AS calories, Url AS url, Image AS image
	FROM(
	SELECT rec_name, rec_ing_num, recipe.Id AS rec_id, recipe.Url, recipe.Image, recipe.Prep_Time, recipe.Calories
	FROM(
	SELECT rec_name, count(*) as rec_ing_num
	FROM(
	SELECT rec.Name AS rec_name, ing.Name AS ing_name
	FROM Recipe AS rec
	JOIN Recipe_Ingredient AS rec_ing
	JOIN Ingredient AS ing
	ON rec_ing.Recipe_Id = rec.Id AND rec_ing.Ingredient_Id = ing.Id
	) x
	GROUP BY rec_name
	) y
	JOIN Recipe recipe
	ON y.rec_name = recipe.Name
	) z
	WHERE rec_ing_num = '{0}'
	LIMIT {1}
	""".format(num, GLOBAL_RESULTS_LIMIT))
	cursor.execute(command)
	return cursorToJSON(cursor)

def apiRecipeByMaxPrepTime(request): # 2
	time = request.GET['prep_to'].replace('+',' ')
	cursor = getCursor()
	cursor.execute(("""
		SELECT rec.Id AS id, rec.Name AS name, rec.Prep_Time AS prep_time, rec.Calories AS calories, rec.Url AS url, rec.Image AS image
		FROM Recipe AS rec
		WHERE TIME(rec.Prep_Time) <= '{0}'
		LIMIT {1}
	""").format(time, GLOBAL_RESULTS_LIMIT))
	return cursorToJSON(cursor)

def apiRecipeByDiet(request): # 3
	diet = request.GET['diet'].replace('+',' ')
	cursor = getCursor()
	cursor.execute(("""
		SELECT rec.Id AS id, rec.Name AS name, rec.Prep_Time AS prep_time, rec.Calories as calories, rec.Url AS url, rec.Image AS image
		FROM Recipe AS rec
		JOIN Recipe_Diet AS rec_diet
		ON rec_diet.Recipe_Id = rec.Id
		JOIN Diet AS diet
		ON diet.Id = rec_diet.Diet_Id
		WHERE diet.Name = '{0}'
		LIMIT {1}
	""").format(diet, GLOBAL_RESULTS_LIMIT))
	return cursorToJSON(cursor)

def apiRecipeByCategory(request): # TODO: Currently not in use
	if not request.is_ajax():
		return jsonApi(300, "Invalid call")
	category = request.GET['category']
	cursor = getCursor()
	cursor.execute(("""
		SELECT recipe.Name AS name, recipe.Url AS url, recipe.Image AS image
		FROM Recipe_Ingredient AS rec_ing
		JOIN(
		SELECT Category_Id, Id
		FROM Ingredient ing
		) x
		ON rec_ing.Ingredient_Id = x.Id
		JOIN (
		SELECT cat.Name AS Category_Name,
		cat.Id
		FROM Category AS cat
		) y
		ON y.Id = x.Category_Id
		JOIN Recipe recipe
		ON recipe.Id = Recipe_Id
		WHERE Category_Name = '{0}'
		LIMIT {1}
	""").format(category, GLOBAL_RESULTS_LIMIT))
	return cursorToJSON(cursor)

def apiRecipeByDishName(request): # 4
	name = request.GET['recipe_name'].replace('+',' ')
	cursor = getCursor()
	cursor.execute(("""
		SELECT rec.Id AS id, rec.Name AS name, rec.Prep_Time AS prep_time, rec.Calories AS calories, rec.Url AS url, rec.Image AS image
		FROM Recipe AS rec
		WHERE rec.Name = '{0}'
	""").format(name))
	return cursorToJSON(cursor)

def apiIngredientsListByRecipiesList(request): # 5
	if not request.is_ajax():
		return jsonApi(300, "Invalid call")
	recipesList = request.GET['selected_recipes'].replace("recipe_n_", "").split("+")
	recipesList += ["" for x in range(5-len(recipesList))]
	cursor = getCursor()
	cursor.execute(("""
	SELECT DISTINCT Ingredient.Name AS ing_name, Category.Name as name, Category.Description as descr
	FROM Ingredient, Recipe, Recipe_Ingredient, Category
	WHERE Recipe.Id = Recipe_Ingredient.Recipe_Id
	and Ingredient.Id = Recipe_Ingredient.Ingredient_Id
	and (Recipe.Id = '{0}' OR Recipe.Id = '{1}' OR Recipe.Id = '{2}' OR Recipe.Id = '{3}' OR Recipe.Id = '{4}')
	order by Category.Name
	""").format(recipesList[0], recipesList[1], recipesList[2], recipesList[3], recipesList[4]))

	result = cursor.fetchall()
	categories = []
	cur_cat_name = result[0]['name']
	cur_cat_desc = result[0]['descr']
	list = []
	# categories = [{"name": ,
	# 			   "desc": ,
	# 			   "list": list}]

	for row in result:
		if row['name'] == cur_cat_name:
			list.append(row['ing_name'])
		else:
			categories.append({"name": cur_cat_name,
						   	   "desc": cur_cat_desc,
						       "list": list.copy()})
			list = []
			cur_cat_name = row['name']
			cur_cat_desc = row['descr']
			list.append(row['ing_name'])

	categories.append({"name": cur_cat_name,
				   	   "desc": cur_cat_desc,
				       "list": list.copy()})

	data = {"categories": categories}

	print("data:\n",data)
	return jsonApi(200, data)

	# data = {"categories": [
	# 		{
	# 			"name": "Sweets",
	# 			"desc": "Sweet products, Candies and Sugar",
	# 			"list": ["Sweet Ingredients #1", "Sweet Ingredients #2", "Sweet Ingredients #3"]
	# 		}, {
	# 			"name": "Vegetable",
	# 			"desc": "Vegetable and Greens",
	# 			"list": ["Vegetable Ingredients #1", "Vegetable Ingredients #2", "Vegetable Ingredients #3", "Vegetable Ingredients #4"]
	# 		}, {
	# 			"name": "Cooking & Baking",
	# 			"desc": "Cooking and Baking products - oils, flours…",
	# 			"list": ["Cooking Ingredients #1", "Cooking Ingredients #2"]
	# 		}
	# 	]}

	return cursorToJSON(cursor)

def apiMealByNumRecipiesAndTotalTime(request):
	if not request.is_ajax():
		return jsonApi(300, "Invalid call")
	numRecipies = request.GET['num_recipes'] # TODO: CHANGE PARAMETER ACCORDING UI
	time = request.GET['time']
	if (numRecipies == 1):
		return apiOneMealByTotalTime(time)
	if (numRecipies == 2):
		return apiTwoMealsByTotalTime(time)
	if (numRecipies == 3):
		return apiThreeMealsByTotalTime(time)
	if (numRecipies == 4):
		return apiFourMealsByTotalTime(time)
	if (numRecipies == 5):
		return apiFiveMealsByTotalTime(time)
	return jsonApi(300, "Invalid call")

def apiOneMealByTotalTime(time):
	cursor = getCursor()
	cursor.execute(("""
	SELECT rec.Name, rec.Prep_Time AS Total_Time, rec.Url, rec.Image
	FROM Recipe rec
	WHERE rec.Prep_Time <= '{0}'
	ORDER BY rec.Prep_Time DESC
	LIMIT 1
	""").format(time))
	return cursorToJSON(cursor)

def apiTwoMealsByTotalTime(time):
	cursor = getCursor()
	cursor.execute(("""
	SELECT x.R1_Name, x.R1_Time, x.R1_Url ,x.R1_Image,
	x.R2_Name, x.R2_Time, x.R2_Url ,x.R2_Image,
	ADDTIME(x.R1_Time, x.R2_Time) AS Total_Time
	FROM(
		SELECT R1.Name AS R1_Name , R1.Prep_Time AS R1_Time, R1.Url AS R1_Url, R1.Image AS R1_Image,
			R2.Name AS R2_Name, R2.Prep_Time AS R2_Time, R2.Url AS R2_Url, R2.Image AS R2_Image
			FROM (
				SELECT Id, Name, Prep_Time, Url, Image FROM Recipe WHERE Prep_Time < '{0}'
				 ) AS R1,
				 (
				SELECT Id, Name, Prep_Time, Url, Image FROM Recipe WHERE Prep_Time < '{0}'
				 ) AS R2
		WHERE ADDTIME(R1.Prep_Time, R2.Prep_Time) <= '{0}' AND R1.Name != R2.Name
		LIMIT {1}
	) x
	ORDER BY Total_Time DESC
	LIMIT 1
	""").format(time, GLOBAL_CALC_RESULTS_LIMITS))
	return cursorToJSON(cursor)

def apiThreeMealsByTotalTime(time):
	cursor = getCursor()
	cursor.execute(("""
	SELECT x.R1_Name, x.R1_Time, x.R1_Url ,x.R1_Image,
	x.R2_Name, x.R2_Time, x.R2_Url ,x.R2_Image,
	x.R3_Name, x.R3_Time, x.R3_Url ,x.R3_Image,
	ADDTIME(ADDTIME(x.R1_Time, x.R2_Time), x.R3_Time) AS Total_Time
	FROM(
		SELECT R1.Name AS R1_Name , R1.Prep_Time AS R1_Time, R1.Url AS R1_Url, R1.Image AS R1_Image,
			R2.Name AS R2_Name, R2.Prep_Time AS R2_Time, R2.Url AS R2_Url, R2.Image AS R2_Image,
			R3.Name AS R3_Name, R3.Prep_Time AS R3_Time, R3.Url AS R3_Url, R3.Image AS R3_Image
			FROM (
				SELECT Id, Name, Prep_Time, Url, Image FROM Recipe WHERE Prep_Time < '{0}'
				 ) AS R1,
				 (
				SELECT Id, Name, Prep_Time, Url, Image FROM Recipe WHERE Prep_Time < '{0}'
				 ) AS R2,
				 (
				SELECT Id, Name, Prep_Time, Url, Image FROM Recipe WHERE Prep_Time < '{0}'
				 ) AS R3
		WHERE ADDTIME(ADDTIME(R1.Prep_Time, R2.Prep_Time), R3.Prep_Time) <= '{0}'
		AND R1.Name != R2.Name AND R1.Name != R3.Name
	AND R2.Name != R3.Name
	LIMIT {1}
	) x
	ORDER BY Total_Time DESC
	LIMIT 1
	""").format(time, GLOBAL_CALC_RESULTS_LIMITS))
	return cursorToJSON(cursor)

def apiFourMealsByTotalTime(time):
	cursor = getCursor()
	cursor.execute(("""
	SELECT x.R1_Name, x.R1_Time, x.R1_Url ,x.R1_Image,
	x.R2_Name, x.R2_Time, x.R2_Url ,x.R2_Image,
	x.R3_Name, x.R3_Time, x.R3_Url ,x.R3_Image,
	x.R4_Name, x.R4_Time, x.R4_Url ,x.R4_Image,
	ADDTIME(ADDTIME(ADDTIME(x.R1_Time, x.R2_Time), x.R3_Time), x.R4_Time) AS Total_Time
	FROM(
		SELECT R1.Name AS R1_Name , R1.Prep_Time AS R1_Time, R1.Url AS R1_Url, R1.Image AS R1_Image,
			R2.Name AS R2_Name, R2.Prep_Time AS R2_Time, R2.Url AS R2_Url, R2.Image AS R2_Image,
			R3.Name AS R3_Name, R3.Prep_Time AS R3_Time, R3.Url AS R3_Url, R3.Image AS R3_Image,
			R4.Name AS R4_Name, R4.Prep_Time AS R4_Time, R4.Url AS R4_Url, R4.Image AS R4_Image
			FROM (
				SELECT Id, Name, Prep_Time, Url, Image FROM Recipe WHERE Prep_Time < '{0}'
				 ) AS R1,
				 (
				SELECT Id, Name, Prep_Time, Url, Image FROM Recipe WHERE Prep_Time < '{0}'
				 ) AS R2,
				 (
				SELECT Id, Name, Prep_Time, Url, Image FROM Recipe WHERE Prep_Time < '{0}'
				 ) AS R3,
				 (
				SELECT Id, Name, Prep_Time, Url, Image FROM Recipe WHERE Prep_Time < '{0}'
				 ) AS R4
		WHERE ADDTIME(ADDTIME(ADDTIME(R1.Prep_Time, R2.Prep_Time), R3.Prep_Time), R4.Prep_Time) <= '{0}'
		AND R1.Name != R2.Name AND R1.Name != R3.Name AND R1.Name != R4.Name
	AND R2.Name != R3.Name AND R2.Name != R4.Name
	AND R3.Name != R4.Name
	LIMIT {1}
	) x
	ORDER BY Total_Time DESC
	LIMIT 1
	""").format(time,GLOBAL_CALC_RESULTS_LIMITS))
	return cursorToJSON(cursor)

def apiFiveMealsByTotalTime(time):
	cursor = getCursor()
	cursor.execute(("""
	SELECT x.R1_Name, x.R1_Time, x.R1_Url ,x.R1_Image,
	x.R2_Name, x.R2_Time, x.R2_Url ,x.R2_Image,
	x.R3_Name, x.R3_Time, x.R3_Url ,x.R3_Image,
	x.R4_Name, x.R4_Time, x.R4_Url ,x.R4_Image,
	x.R5_Name, x.R5_Time, x.R5_Url ,x.R5_Image,
	ADDTIME(ADDTIME(ADDTIME(ADDTIME(x.R1_Time, x.R2_Time), x.R3_Time), x.R4_Time), x.R5_TIME) AS Total_Time
	FROM(
		SELECT R1.Name AS R1_Name , R1.Prep_Time AS R1_Time, R1.Url AS R1_Url, R1.Image AS R1_Image,
			R2.Name AS R2_Name, R2.Prep_Time AS R2_Time, R2.Url AS R2_Url, R2.Image AS R2_Image,
			R3.Name AS R3_Name, R3.Prep_Time AS R3_Time, R3.Url AS R3_Url, R3.Image AS R3_Image,
			R4.Name AS R4_Name, R4.Prep_Time AS R4_Time, R4.Url AS R4_Url, R4.Image AS R4_Image,
			R5.Name AS R5_Name, R5.Prep_Time AS R5_Time, R5.Url AS R5_Url, R5.Image AS R5_Image
		FROM (
			SELECT Id, Name, Prep_Time, Url, Image FROM Recipe WHERE Prep_Time < '{0}'
			 ) AS R1,
			 (
			SELECT Id, Name, Prep_Time, Url, Image FROM Recipe WHERE Prep_Time < '{0}'
			 ) AS R2,
			 (
			SELECT Id, Name, Prep_Time, Url, Image FROM Recipe WHERE Prep_Time < '{0}'
			 ) AS R3,
			 (
			SELECT Id, Name, Prep_Time, Url, Image FROM Recipe WHERE Prep_Time < '{0}'
			 ) AS R4,
			 (
			SELECT Id, Name, Prep_Time, Url, Image FROM Recipe WHERE Prep_Time < '{0}'
			 ) AS R5
		WHERE ADDTIME(ADDTIME(ADDTIME(ADDTIME(R1.Prep_Time, R2.Prep_Time),
		 R3.Prep_Time), R4.Prep_Time), R5.Prep_Time) <= '{0}'
		AND R1.Name != R2.Name AND R1.Name != R3.Name AND R1.Name != R4.Name AND R1.Name != R5.Name
	AND R2.Name != R3.Name AND R2.Name != R4.Name AND R2.Name != R5.Name
	AND R3.Name != R4.Name AND R3.Name != R5.Name
		AND R4.Name != R5.Name
	LIMIT {1}
	) x
	ORDER BY Total_Time DESC
	LIMIT 1
	""").format(time,GLOBAL_CALC_RESULTS_LIMITS))
	return cursorToJSON(cursor)

def apiRecipeByIngredientList(request):
	if not request.is_ajax():
		return jsonApi(300, "Invalid call")
	list = request.GET['ingredients_inc'].split("+") # TODO: CHANGE PARAMETER ACCORDING UI
	if(len(list) == 1):
		return apiRecipeByOneIngredient(list)
	if(len(list) == 2):
		return apiRecipeByTwoIngredients(list)
	if(len(list) == 3):
		return apiRecipeByThreeIngredients(list)
	if(len(list) == 4):
		return apiRecipeByFourIngredients(list)
	if(len(list) == 5):
		return apiRecipeByFiveIngredients(list)
	return jsonApi(300, "Invalid Call")

def apiRecipeByOneIngredient(list):
	cursor = getCursor()
	cursor.execute(("""
	SELECT distinct d.Name AS rec_name, z.rec_ing_num, d.Url, d.Image
	FROM Recipe AS d
	JOIN Ingredient AS ing
	INNER JOIN (
	SELECT Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name
	FROM(
	SELECT * FROM Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x1
	) AS i1
	ON d.Id = i1.rec_id
	AND i1.ing_name = '{0}'
	join (
	SELECT rec_name, rec_ing_num, recipe.Id AS rec_id
	FROM(
	SELECT rec_name, count(*) as rec_ing_num
	FROM(
	SELECT rec.Name AS rec_name, ing.Name AS ing_name
	FROM Recipe AS rec
	JOIN Recipe_Ingredient AS rec_ing
	JOIN Ingredient AS ing
	ON rec_ing.Recipe_Id = rec.Id AND rec_ing.Ingredient_Id = ing.Id
	) x
	GROUP BY rec_name
	) y
	JOIN Recipe recipe
	ON y.rec_name = recipe.Name
	) z
	ON d.Id = z.rec_id
	WHERE z.rec_ing_num = 1
	""").format(list[0]))
	return cursorToJSON(cursor)

def apiRecipeByTwoIngredients(list):
	cursor = getCursor()
	cursor.execute(("""
	SELECT distinct d.Name AS rec_name, z.rec_ing_num, d.Url, d.Image
	FROM Recipe AS d
	JOIN Ingredient AS ing
	INNER JOIN (
	SELECT Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name
	FROM(
	SELECT * FROM Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x1
	) AS i1
	ON d.Id = i1.rec_id
	AND i1.ing_name = '{0}'
	INNER JOIN (
	SELECT Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	SELECT * FROM Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x2
	) AS i2
	ON d.Id = i2.rec_id
	AND i2.ing_name = '{1}'
	join (
	SELECT rec_name, rec_ing_num, recipe.Id AS rec_id
	FROM(
	SELECT rec_name, count(*) as rec_ing_num
	FROM(
	SELECT rec.Name AS rec_name, ing.Name AS ing_name
	FROM Recipe AS rec
	JOIN Recipe_Ingredient AS rec_ing
	JOIN Ingredient AS ing
	ON rec_ing.Recipe_Id = rec.Id AND rec_ing.Ingredient_Id = ing.Id
	) x
	GROUP BY rec_name
	) y
	JOIN Recipe recipe
	ON y.rec_name = recipe.Name
	) z
	ON d.Id = z.rec_id
	WHERE z.rec_ing_num = 2
	""").format(list[0], list[1]))
	return cursorToJSON(cursor)

def apiRecipeByThreeIngredients(list):
	cursor = getCursor()
	cursor.execute(("""
	SELECT distinct d.Name AS rec_name, z.rec_ing_num, d.Url, d.Image
	FROM Recipe AS d
	JOIN Ingredient AS ing
	INNER JOIN (
	SELECT Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name
	FROM(
	SELECT * FROM Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x1
	) AS i1
	ON d.Id = i1.rec_id
	AND i1.ing_name = '{0}'
	INNER JOIN (
	SELECT Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	SELECT * FROM Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x2
	) AS i2
	ON d.Id = i2.rec_id
	AND i2.ing_name = '{1}'
	INNER JOIN (
	SELECT Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	SELECT * FROM Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x3
	) AS i3
	ON d.Id = i3.rec_id
	AND i3.ing_name = '{2}'
	join (
	SELECT rec_name, rec_ing_num, recipe.Id AS rec_id
	FROM(
	SELECT rec_name, count(*) as rec_ing_num
	FROM(
	SELECT rec.Name AS rec_name, ing.Name AS ing_name
	FROM Recipe AS rec
	JOIN Recipe_Ingredient AS rec_ing
	JOIN Ingredient AS ing
	ON rec_ing.Recipe_Id = rec.Id AND rec_ing.Ingredient_Id = ing.Id
	) x
	GROUP BY rec_name
	) y
	JOIN Recipe recipe
	ON y.rec_name = recipe.Name
	) z
	ON d.Id = z.rec_id
	WHERE z.rec_ing_num = 3
	""").format(list[0], list[1], list[2]))
	return cursorToJSON(cursor)

def apiRecipeByFourIngredients(list):
	cursor = getCursor()
	cursor.execute(("""
	SELECT distinct d.Name AS rec_name, z.rec_ing_num, d.Url, d.Image
	FROM Recipe AS d
	JOIN Ingredient AS ing

	INNER JOIN (
	SELECT Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name
	FROM(
	SELECT * FROM Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x1
	) AS i1
	ON d.Id = i1.rec_id
	AND i1.ing_name = '{0}'
	INNER JOIN (
	SELECT Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	SELECT * FROM Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x2
	) AS i2
	ON d.Id = i2.rec_id
	AND i2.ing_name = '{1}'
	INNER JOIN (
	SELECT Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	SELECT * FROM Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x3
	) AS i3
	ON d.Id = i3.rec_id
	AND i3.ing_name = '{2}'
	INNER JOIN (
	SELECT Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	SELECT * FROM Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x4
	) AS i4
	ON d.Id = i4.rec_id
	AND i4.ing_name = '{3}'
	join (
	SELECT rec_name, rec_ing_num, recipe.Id AS rec_id
	FROM(
	SELECT rec_name, count(*) as rec_ing_num
	FROM(
	SELECT rec.Name AS rec_name, ing.Name AS ing_name
	FROM Recipe AS rec
	JOIN Recipe_Ingredient AS rec_ing
	JOIN Ingredient AS ing
	ON rec_ing.Recipe_Id = rec.Id AND rec_ing.Ingredient_Id = ing.Id
	) x
	GROUP BY rec_name
	) y
	JOIN Recipe recipe
	ON y.rec_name = recipe.Name
	) z
	ON d.Id = z.rec_id
	WHERE z.rec_ing_num = 4
	""").format(list[0], list[1], list[2], list[3]))
	return cursorToJSON(cursor)

def apiRecipeByFiveIngredients(list):
	cursor = getCursor()
	cursor.execute(("""
	SELECT distinct d.Name AS rec_name, z.rec_ing_num, d.Url, d.Image
	FROM Recipe AS d
	JOIN Ingredient AS ing
	INNER JOIN (
	SELECT Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name
	FROM(
	SELECT * FROM Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x1
	) AS i1
	ON d.Id = i1.rec_id
	AND i1.ing_name = '{0}'
	INNER JOIN (
	SELECT Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	SELECT * FROM Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x2
	) AS i2
	ON d.Id = i2.rec_id
	AND i2.ing_name = '{1}'
	INNER JOIN (
	SELECT Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	SELECT * FROM Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x3
	) AS i3
	ON d.Id = i3.rec_id
	AND i3.ing_name = '{2}'
	INNER JOIN (
	SELECT Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	SELECT * FROM Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x4
	) AS i4
	ON d.Id = i4.rec_id
	AND i4.ing_name = '{3}'
	INNER JOIN (
	SELECT Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	SELECT * FROM Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x5
	) AS i5
	ON d.Id = i5.rec_id
	AND i5.ing_name = '{4}'
	join (
	SELECT rec_name, rec_ing_num, recipe.Id AS rec_id
	FROM(
	SELECT rec_name, count(*) as rec_ing_num
	FROM(
	SELECT rec.Name AS rec_name, ing.Name AS ing_name
	FROM Recipe AS rec
	JOIN Recipe_Ingredient AS rec_ing
	JOIN Ingredient AS ing
	ON rec_ing.Recipe_Id = rec.Id AND rec_ing.Ingredient_Id = ing.Id
	) x
	GROUP BY rec_name
	) y
	JOIN Recipe recipe
	ON y.rec_name = recipe.Name
	) z
	ON d.Id = z.rec_id
	WHERE z.rec_ing_num = 5

	""").format(list[0], list[1], list[2], list[3], list[4]))
	return cursorToJSON(cursor)

####################################################################
####	Functions:						####
####################################################################
# 1)  def apiGetDiets(request):					####
# 2)  def apiIngredientsSuggestion(request):			####
# 3)  def apiIngredients(request):				####
# 4)  def apiRecipesSuggestion(request):			####
# 5)  def apiSearchMeals(request):				####
# 6)  def apiSearchRecipes(request):				####
####################################################################
def apiGetDiets(request):
	if (request.method != "GET") or (not request.is_ajax()):
		return jsonApi(300, "Invalid call")
	data = {"list": [
			{"name": "balanced",		"desc": "Protein/Fat/Carb values in 15/35/50 ratio"},
			{"name": "high-protein",	"desc": "More then 50% of total calories from proteins"},
			{"name": "alcohol-free",	"desc": "No alcohol used or contained"}
		]}
	return jsonApi(200, data)

def apiIngredientsSuggestion(request):
	if (request.method != "GET") or (not request.is_ajax()):
		return jsonApi(300, "Invalid call")
	data = {"suggestions": [
			{"name": "Apple"},
			{"name": "Lemon"},
			{"name": "Milk"}
		]}
	print("data:\n",data)
	return jsonApi(200, data)

def apiIngredients(request):
	return(apiIngredientsListByRecipiesList(request))

	# if (request.method != "GET") or (not request.is_ajax()):
	# 	return jsonApi(300, "Invalid call")
	# data = {"categories": [
	# 		{
	# 			"name": "Sweets",
	# 			"desc": "Sweet products, Candies and Sugar",
	# 			"list": ["Sweet Ingredients #1", "Sweet Ingredients #2", "Sweet Ingredients #3"]
	# 		}, {
	# 			"name": "Vegetable",
	# 			"desc": "Vegetable and Greens",
	# 			"list": ["Vegetable Ingredients #1", "Vegetable Ingredients #2", "Vegetable Ingredients #3", "Vegetable Ingredients #4"]
	# 		}, {
	# 			"name": "Cooking & Baking",
	# 			"desc": "Cooking and Baking products - oils, flours…",
	# 			"list": ["Cooking Ingredients #1", "Cooking Ingredients #2"]
	# 		}
	# 	]}
	# return jsonApi(200, data)

def apiRecipesSuggestion(request):
	if (request.method != "GET") or (not request.is_ajax()):
		return jsonApi(300, "Invalid call")
	q = request.GET['q']
	cursor = getCursor()
	cursor.execute(("""
	Select rec.Name AS name, rec.Calories AS calories
	From Recipe AS rec
	Where rec.Name like '{0}%'
	""").format(q))
	rv = cursor.fetchall()
	data = {"suggestions": rv}
	return jsonApi(200, data)

def apiSearchMeals(request):
	if (request.method != "GET") or (not request.is_ajax()):
		return jsonApi(300, "Invalid call")
	data = {"results": 4,
		"meals": [[
				{"id": 1, "name": "Balsamic-Glazed Steak Rolls"},
				{"id": 2, "name": "Mongolian Glazed Steak"},
				{"id": 3, "name": "Recipe name number 3"},
				{"id": 4, "name": "Recipe name number 4"}
			],[
				{"id": 5, "name": "Recipe name number 5"},
				{"id": 3, "name": "Recipe name number 3"}
			],[
				{"id": 5, "name": "Recipe name number 5"},
				{"id": 2, "name": "Mongolian Glazed Steak"}
			],[
				{"id": 3, "name": "Recipe name number 3"},
				{"id": 4, "name": "Recipe name number 4"},
				{"id": 5, "name": "Recipe name number 5"},
				{"id": 6, "name": "Recipe name number 6"},
				{"id": 7, "name": "Recipe name number 7"}
			]
		]}
	return jsonApi(200, data)

def apiSearchRecipes(request):
	if (request.method != "GET") or (not request.is_ajax()):
		return jsonApi(300, "Invalid call")
	if (request.GET['recipe_name'] != ''):
		return apiRecipeByDishName(request)
	if (request.GET['ingredients_max'] != '0'):
		return apiRecipeByNumOfIngredients(request)
	if (request.GET['prep_to'] != '180'):
		return apiRecipeByMaxPrepTime(request)
	if (request.GET['diet'] != 'any'):
		return apiRecipeByDiet(request)
	# if ('num_recipes' in request.GET and 'time' in request.GET): # TODO: CHANGE PARAMETER ACCORDING UI
	# 	return apiMealByNumRecipiesAndTotalTime(request)
	if (request.GET['ingredients_inc'] != ''):
		return apiRecipeByIngredientList(request)
	if ('selected_recipes' in request.GET):
		return apiIngredientsListByRecipiesList(request)
	else:
		return apiDefaultResponse(request)
