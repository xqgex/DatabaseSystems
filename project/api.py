# -*- coding: utf-8 -*-
# import json
# from project.views import jsonApi

# def apiGetDiets(request):
# 	data = {"list": [
# 			{"name": "balanced",		"desc": "Protein/Fat/Carb values in 15/35/50 ratio"},
# 			{"name": "high-protein",	"desc": "More then 50% of total calories from proteins"},
# 			{"name": "alcohol-free",	"desc": "No alcohol used or contained"}
# 		]}
# 	return jsonApi(200, data)
#
# def apiIngredientsSuggestion(request):
# 	if not request.is_ajax():
# 		return jsonApi(300, "Invalid call")
# 	data = {"suggestions": [
# 			{"name": "Apple"},
# 			{"name": "Lemon"},
# 			{"name": "Milk"}
# 		]}
# 	return jsonApi(200, data)
#
# def apiRecipesSuggestion(request):
# 	if not request.is_ajax():
# 		return jsonApi(300, "Invalid call")
# 	data = {"suggestions": [
# 			{"name": "Hot Apple Pie",			"calories": "289"},
# 			{"name": "Sparkling Apple Cocktail recioes",	"calories": "609"},
# 			{"name": "Apple-Lemon-Ginger Juice",		"calories": "254"}
# 		]}
# 	return jsonApi(200, data)
#
# def apiSearchRecipes(request):
# 	if not request.is_ajax():
# 		return jsonApi(300, "Invalid call")
# 	data = {"results": 45321,
# 		"items": [
# 			{"id": 1, "name": "Balsamic-Glazed Steak Rolls", "prep_time": "02:15:00", "calories": 1999, "url": "https://Lorem.ipsum", "image": "https://images-gmi-pmc.edge-generalmills.com/7455fc0a-ffad-4526-8b68-e1a8b179914e.jpg"},
# 			{"id": 2, "name": "Mongolian Glazed Steak", "prep_time": "01:00:00", "calories": 2001, "url": "https://Lorem.at.ipsum", "image": "https://s3.amazonaws.com/supercook-thumbs/363402.jpg"},
# 			{"id": 3, "name": "Balsamic-Glazed Steak Rolls", "prep_time": "02:15:00", "calories": 1999, "url": "https://Lorem.ipsum", "image": "https://images-gmi-pmc.edge-generalmills.com/7455fc0a-ffad-4526-8b68-e1a8b179914e.jpg"},
# 			{"id": 4, "name": "Mongolian Glazed Steak", "prep_time": "01:00:00", "calories": 2001, "url": "https://Lorem.at.ipsum", "image": "https://s3.amazonaws.com/supercook-thumbs/363402.jpg"},
# 			{"id": 5, "name": "Balsamic-Glazed Steak Rolls", "prep_time": "02:15:00", "calories": 1999, "url": "https://Lorem.ipsum", "image": "https://images-gmi-pmc.edge-generalmills.com/7455fc0a-ffad-4526-8b68-e1a8b179914e.jpg"},
# 			{"id": 6, "name": "Mongolian Glazed Steak", "prep_time": "01:00:00", "calories": 2001, "url": "https://Lorem.at.ipsum", "image": "https://s3.amazonaws.com/supercook-thumbs/363402.jpg"}
# 		]}
# 	return jsonApi(200, data)

# -*- coding: utf-8 -*-
import json
from project.views import jsonApi
import mysql.connector
import pymysql.cursors

GLOBAL_RESULTS_LIMIT = 100
GLOBAL_CALC_RESULTS_LIMITS = 10000

def getCursor():
	# connection2 = mdb.connect('localhost', 'DbMysql14', 'DbMysql14', 'DbMysql14', 3305)
	connection = pymysql.connect(host='localhost',
								 port=3305,
	                             user='DbMysql14',
	                             password='DbMysql14',
	                             db='DbMysql14',
								 charset='utf8mb4',
                             	 cursorclass=pymysql.cursors.DictCursor)
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
	res = apiRecipeByMaxPrepTime('00:04:00')

	# print(res)

	data = {"suggestions": [
			{ "value": "Arab Emirates", "data": "AE" },
			{ "value": "United Kingdom", "data": "UK" },
			{ "value": "United States", "data": "US" }
		]}
	return jsonApi(200, data)

def cursorToJSON(cursor):
   result = json.dumps(cursor.fetchall(), indent=4)
   print(result)
   return result

def apiRecipeByNumOfIngredients(num):
	# if not request.is_ajax():
	# 	return jsonApi(300, "Invalid call")
	cursor = getCursor()
	command = ("""
	select rec_name, rec_ing_num, Url, Image
	from(
	select rec_name, rec_ing_num, recipe.Id AS rec_id, recipe.Url, recipe.Image
	from(
	SELECT rec_name, count(*) as rec_ing_num
	FROM(
	select rec.Name AS rec_name, ing.Name AS ing_name
	FROM Recipe AS rec
	JOIN Recipe_Ingredient AS rec_ing
	JOIN Ingredient AS ing
	ON rec_ing.Recipe_Id =  rec.Id AND rec_ing.Ingredient_Id = ing.Id
	) x
	GROUP BY rec_name
	) y
	JOIN Recipe recipe
	ON y.rec_name = recipe.Name
	) z
	WHERE rec_ing_num = '{0}'
	LIMIT '{1}'
	""".format(num, GLOBAL_RESULTS_LIMIT))
	cursor.execute(command)
	return cursorToJSON(cursor)

def apiRecipeByMaxPrepTime(time):
	cursor = getCursor()
	cursor.execute(("""
		SELECT json_object('Recipe_Name', rec.Name,'Prep_Time', rec.Prep_Time)
		FROM Recipe AS rec
		WHERE TIME(rec.Prep_Time) <= '{0}'
		LIMIT {1}
	""").format(time, GLOBAL_RESULTS_LIMIT))
	return cursorToJSON(cursor)

def apiRecipeByDiet(diet):
	cursor = getCursor()
	cursor.execute(("""
		SELECT diet.Name AS Diet_Name, rec.Name AS Recipe_Name, rec.Url, rec.Image
		rec.Calories, rec.Url, rec.Image
		FROM Recipe AS rec
		JOIN Recipe_Diet AS rec_diet
		ON rec_diet.Recipe_Id = rec.Id
		JOIN Diet AS diet
		ON diet.Id = rec_diet.Diet_Id
		WHERE diet.Name = '{0}'
		LIMIT {1}
	""").format(diet, GLOBAL_RESULTS_LIMIT))
	return cursorToJSON(cursor)

def apiRecipeByCategory(category):
	cursor = getCursor()
	cursor.execute(("""
		SELECT y.Category_Name, recipe.Name AS Recipe_Name, recipe.Url, recipe.Image
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

def apiRecipeByDishName(name):
	cursor = getCursor()
	cursor.execute(("""
		SELECT rec.Name AS Recipe_Name,
		rec.Url, rec.Image
		FROM Recipe AS rec
		WHERE rec.Name = '{0}'
	""").format(name))
	return cursorToJSON(cursor)

def apiMealByNumRecipiesAndTotalTime(numRecipies, time):
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
	SELECT rec.Name, rec.Prep_Time AS Total_Time
	FROM Recipe rec
	WHERE rec.Prep_Time <= '{0}'
	ORDER BY rec.Prep_Time DESC
	LIMIT 1
	""").format(time))
	# data = cursor.fetchall()
	# print(data)
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
		LIMIT '{1}'
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
	(ADDTIME(ADDTIME(x.R1_Time, x.R2_Time), x.R3_Time) AS Total_Time
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
        LIMIT '{1}'
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
        LIMIT '{1}'
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
        LIMIT '{1}'
	) x
	ORDER BY Total_Time DESC
	LIMIT 1
	""").format(time,GLOBAL_CALC_RESULTS_LIMITS))
	return cursorToJSON(cursor)

def apiRecipeByIngredientList(list):
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
	select Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name
	FROM(
	select * from Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x1
	) AS i1
	  ON d.Id = i1.rec_id
	  AND i1.ing_name = '{0}'
	join (
	select rec_name, rec_ing_num, recipe.Id AS rec_id
	from(
	SELECT rec_name, count(*) as rec_ing_num
	FROM(
	select rec.Name AS rec_name, ing.Name AS ing_name
	FROM Recipe AS rec
	JOIN Recipe_Ingredient AS rec_ing
	JOIN Ingredient AS ing
	ON rec_ing.Recipe_Id =  rec.Id AND rec_ing.Ingredient_Id = ing.Id
	) x
	GROUP BY rec_name
	) y
	JOIN Recipe recipe
	ON y.rec_name = recipe.Name
	) z
	ON d.Id = z.rec_id
	where z.rec_ing_num = 1
	""").format(list[0]))
	return cursorToJSON(cursor)

def apiRecipeByTwoIngredients(list):
	cursor = getCursor()
	cursor.execute(("""
	SELECT distinct d.Name AS rec_name, z.rec_ing_num, d.Url, d.Image
	FROM Recipe AS d
	JOIN Ingredient AS ing

	INNER JOIN (
	select Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name
	FROM(
	select * from Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x1
	) AS i1
	  ON d.Id = i1.rec_id
	  AND i1.ing_name = '{0}'

	INNER JOIN (
	select Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	select * from Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x2
	) AS i2
	  ON d.Id = i2.rec_id
	  AND i2.ing_name = '{1}'

	join (
	select rec_name, rec_ing_num, recipe.Id AS rec_id
	from(
	SELECT rec_name, count(*) as rec_ing_num
	FROM(
	select rec.Name AS rec_name, ing.Name AS ing_name
	FROM Recipe AS rec
	JOIN Recipe_Ingredient AS rec_ing
	JOIN Ingredient AS ing
	ON rec_ing.Recipe_Id =  rec.Id AND rec_ing.Ingredient_Id = ing.Id
	) x
	GROUP BY rec_name
	) y
	JOIN Recipe recipe
	ON y.rec_name = recipe.Name
	) z
	ON d.Id = z.rec_id
	where z.rec_ing_num = 2

	""").format(list[0], list[1]))
	return cursorToJSON(cursor)

def apiRecipeByThreeIngredients(list):
	cursor = getCursor()
	cursor.execute(("""
SELECT distinct d.Name AS rec_name, z.rec_ing_num, d.Url, d.Image
FROM Recipe AS d
JOIN Ingredient AS ing

INNER JOIN (
select Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name
FROM(
select * from Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
ON ing.Id = rec_ing.Ingredient_Id) x1
) AS i1
  ON d.Id = i1.rec_id
  AND i1.ing_name = '{0}'

INNER JOIN (
select Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
select * from Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
ON ing.Id = rec_ing.Ingredient_Id) x2
) AS i2
  ON d.Id = i2.rec_id
  AND i2.ing_name = '{1}'

INNER JOIN (
select Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
select * from Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
ON ing.Id = rec_ing.Ingredient_Id) x3
) AS i3
ON d.Id = i3.rec_id
AND i3.ing_name = '{2}'

join (
select rec_name, rec_ing_num, recipe.Id AS rec_id
from(
SELECT rec_name, count(*) as rec_ing_num
FROM(
select rec.Name AS rec_name, ing.Name AS ing_name
FROM Recipe AS rec
JOIN Recipe_Ingredient AS rec_ing
JOIN Ingredient AS ing
ON rec_ing.Recipe_Id =  rec.Id AND rec_ing.Ingredient_Id = ing.Id
) x
GROUP BY rec_name
) y
JOIN Recipe recipe
ON y.rec_name = recipe.Name
) z
ON d.Id = z.rec_id
where z.rec_ing_num = 3

""").format(list[0], list[1], list[2]))
	return cursorToJSON(cursor)

def apiRecipeByFourIngredients(list):
	cursor = getCursor()
	cursor.execute(("""
	SELECT distinct d.Name AS rec_name, z.rec_ing_num, d.Url, d.Image
	FROM Recipe AS d
	JOIN Ingredient AS ing

	INNER JOIN (
	select Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name
	FROM(
	select * from Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x1
	) AS i1
	  ON d.Id = i1.rec_id
	  AND i1.ing_name = '{0}'

	INNER JOIN (
	select Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	select * from Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x2
	) AS i2
	  ON d.Id = i2.rec_id
	  AND i2.ing_name = '{1}'

	INNER JOIN (
	select Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	select * from Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x3
	) AS i3
	ON d.Id = i3.rec_id
	AND i3.ing_name = '{2}'

	INNER JOIN (
	select Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	select * from Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x4
	) AS i4
	ON d.Id = i4.rec_id
	AND i4.ing_name = '{3}'

	join (
	select rec_name, rec_ing_num, recipe.Id AS rec_id
	from(
	SELECT rec_name, count(*) as rec_ing_num
	FROM(
	select rec.Name AS rec_name, ing.Name AS ing_name
	FROM Recipe AS rec
	JOIN Recipe_Ingredient AS rec_ing
	JOIN Ingredient AS ing
	ON rec_ing.Recipe_Id =  rec.Id AND rec_ing.Ingredient_Id = ing.Id
	) x
	GROUP BY rec_name
	) y
	JOIN Recipe recipe
	ON y.rec_name = recipe.Name
	) z
	ON d.Id = z.rec_id
	where z.rec_ing_num = 4

	""").format(list[0], list[1], list[2], list[3]))
	return cursorToJSON(cursor)

def apiRecipeByFiveIngredients(list):
	cursor = getCursor()
	cursor.execute(("""
	SELECT distinct d.Name AS rec_name, z.rec_ing_num, d.Url, d.Image
	FROM Recipe AS d
	JOIN Ingredient AS ing

	INNER JOIN (
	select Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name
	FROM(
	select * from Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x1
	) AS i1
	  ON d.Id = i1.rec_id
	  AND i1.ing_name = '{0}'

	INNER JOIN (
	select Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	select * from Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x2
	) AS i2
	  ON d.Id = i2.rec_id
	  AND i2.ing_name = '{1}'

	INNER JOIN (
	select Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	select * from Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x3
	) AS i3
	ON d.Id = i3.rec_id
	AND i3.ing_name = '{2}'

	INNER JOIN (
	select Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	select * from Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x4
	) AS i4
	ON d.Id = i4.rec_id
	AND i4.ing_name = '{3}'

	INNER JOIN (
	select Recipe_Id AS rec_id, Ingredient_Id AS ing_id, Name AS ing_name FROM(
	select * from Recipe_Ingredient AS rec_ing JOIN Ingredient AS ing
	ON ing.Id = rec_ing.Ingredient_Id) x5
	) AS i5
	ON d.Id = i5.rec_id
	AND i5.ing_name = '{4}'

	join (
	select rec_name, rec_ing_num, recipe.Id AS rec_id
	from(
	SELECT rec_name, count(*) as rec_ing_num
	FROM(
	select rec.Name AS rec_name, ing.Name AS ing_name
	FROM Recipe AS rec
	JOIN Recipe_Ingredient AS rec_ing
	JOIN Ingredient AS ing
	ON rec_ing.Recipe_Id =  rec.Id AND rec_ing.Ingredient_Id = ing.Id
	) x
	GROUP BY rec_name
	) y
	JOIN Recipe recipe
	ON y.rec_name = recipe.Name
	) z
	ON d.Id = z.rec_id
	where z.rec_ing_num = 5

	""").format(list[0], list[1], list[2], list[3], list[4]))
	return cursorToJSON(cursor)
