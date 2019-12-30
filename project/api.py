#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime, json
import pymysql.cursors
from project.views import jsonApi

############################################################################
####	Functions:							####
############################################################################
# 1)  def getCursor()							####
# 2)  apiIngredients(request)						####
# 3)  apiGetDiets(request)						####
# 4)  apiIngredientsSuggestion(request)					####
# 5)  apiRecipesSuggestion(request)					####
# 6)  apiSearchMeals(request)						####
# 7)  fetchRecipies(request, recipes_per_meal) 				####
# 8)  apiSearchRecipes(request)						####
# 9)  getSortBy(param)							####
# 10) recipe_query(name_string, diet_string,				####
# 	  prep_time_lower_bound, prep_time_upper_bound, ingr_in,	####
#	  ingr_out, page, sort_by, sort_order, recipes_per_meal)	####
############################################################################
def getCursor():
	# LOCAL :
	# connection = pymysql.connect(host="localhost", # XXX DEBUG XXX
	# 				port=3305, # XXX DEBUG XXX
	# 				user="DbMysql14", # XXX DEBUG XXX
	# 				password="DbMysql14", # XXX DEBUG XXX
	# 				db="DbMysql14", # XXX DEBUG XXX
	# 				charset="utf8mb4", # XXX DEBUG XXX
	# 				cursorclass=pymysql.cursors.DictCursor) # XXX DEBUG XXX
	# PROD :
	connection = pymysql.connect(host="mysqlsrv1.cs.tau.ac.il",
					port=3306,
					user="DbMysql14",
					password="DbMysql14",
					db="DbMysql14",
					charset="utf8mb4",
					cursorclass=pymysql.cursors.DictCursor)
	return connection.cursor()

def apiIngredients(request):
	if (request.method != "GET") or (not request.is_ajax()):
		return jsonApi(300, "Invalid call")
	recipesList = request.GET["selected_recipes"].replace("recipe_n_", "").split("+")
	query_completion = "( "
	for i in range (len(recipesList)-1):
		query_completion += "rec.Id = {0} OR ".format(recipesList[i])
	query_completion += "rec.Id = {0} )".format(recipesList[len(recipesList)-1])
	#print("quer-comp:\n", query_completion) # XXX DEBUG XXX
	cursor = getCursor()
	query = ("""
	SELECT DISTINCT ing.Name AS ing_name, cat.Name as name, cat.Description as descr
	FROM Ingredient as ing
	INNER JOIN Category as cat
	ON ing.Category_Id = cat.Id
	INNER JOIN Recipe_Ingredient as rec_ing
	ON ing.Id = rec_ing.Ingredient_Id
	INNER JOIN Recipe as rec
	ON rec.Id = rec_ing.Recipe_Id
	WHERE {0}
	order by cat.Name
	""").format(query_completion)
	#print("query:\n", query) # XXX DEBUG XXX
	cursor.execute(query)
	result = cursor.fetchall()
	#print("result:\n", result) # XXX DEBUG XXX
	categories = []
	cur_cat_name = result[0]["name"]
	cur_cat_desc = result[0]["descr"]
	cur_list = []
	for row in result:
		if row["name"] == cur_cat_name:
			cur_list.append(row["ing_name"])
		else:
			list_copy = list(cur_list)
			categories.append({"name": cur_cat_name, "descr": cur_cat_desc, "list": list_copy})
			cur_list = []
			cur_cat_name = row["name"]
			cur_cat_desc = row["descr"]
			cur_list.append(row["ing_name"])
	list_copy = list(cur_list)
	categories.append({"name": cur_cat_name, "descr": cur_cat_desc, "list": list_copy})
	data = {"categories": categories}
	# print("data:\n", data) # XXX DEBUG XXX
	return jsonApi(200, data)

def apiGetDiets(request):
	if (request.method != "GET") or (not request.is_ajax()):
		return jsonApi(300, "Invalid call")
	cursor = getCursor()
	cursor.execute("""
	SELECT Name as name, Description as descr
	FROM Diet
	""")
	data = {"list": cursor.fetchall()}
	return jsonApi(200, data)

def apiIngredientsSuggestion(request):
	if (request.method != "GET") or (not request.is_ajax()):
		return jsonApi(300, "Invalid call")
	q = request.GET["q"]
	cursor = getCursor()
	cursor.execute(("""
	Select ing.Name AS name
	From Ingredient as ing
	Where ing.Name like '{0}%'
	""").format(q))
	rv = cursor.fetchall()
	data = {"suggestions": rv}
	return jsonApi(200, data)

def apiRecipesSuggestion(request):
	if (request.method != "GET") or (not request.is_ajax()):
		return jsonApi(300, "Invalid call")
	q = request.GET["q"]
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
	recipes_per_meal = request.GET["recipes_per_meal"]
	result_orig = fetchRecipies("SearchMeals", request, -1)
	result = fetchRecipies("SearchMeals", request, recipes_per_meal)
	meals = []
	cur_meal = []
	i = 0
	j = 0
	for item in result:
		cur_meal.append(item)
		i += 1
		j += 1
		if (i == int(recipes_per_meal)):
			meals.append(list(cur_meal))
			i = 0
			cur_meal = []
	data = {"results": len(result_orig)//int(recipes_per_meal), "meals": meals}
	# print("data: ", data) # XXX DEBUG XXX
	return jsonApi(200, data)

def fetchRecipies(search_type, request, recipes_per_meal):
	if (request.method != "GET") or (not request.is_ajax()):
		return jsonApi(300, "Invalid call")
	if ("invalid" in request.GET.values()):
		print("Got invalid parameters on GET call")
		return jsonApi(300, "Invalid call")
	# EXAMPLE 1: recipe_name=&diet=any&prep_from=0&prep_to=180&ingredients_inc=&ingredients_exc=&recipes_per_meal=5&sort_by=sort_by_name&sort_order=desc&page=0
	# EXAMPLE 2: recipe_name=&prep_from=invalid&prep_to=invalid&ingredients_inc=&ingredients_exc=&sort_by=sort_by_name&sort_order=desc&page=0
	# PARAMETERS:
	if search_type == "SearchMeals":
		recipe_name = ""
		diet = "any"
	else:
		recipe_name = request.GET["recipe_name"]
		diet = request.GET["diet"]
	prep_from = "\'{0}\'".format(datetime.timedelta(minutes=int(request.GET["prep_from"])))
	prep_to = "\'{0}\'".format(datetime.timedelta(minutes=int(request.GET["prep_to"])))
	ingredients_inc = request.GET["ingredients_inc"].split("+")
	ingredients_exc = request.GET["ingredients_exc"].split("+")
	sort_by = getSortBy(request.GET["sort_by"].replace("sort_by_", ""))
	sort_order = request.GET["sort_order"]
	page = request.GET["page"]
	# print("params: ", recipe_name, " ", diet, " ", prep_from, " ", prep_to, " ", ingredients_inc, " ", ingredients_exc, " ", page) # XXX DEBUG XXX
	query = recipe_query(recipe_name, diet, prep_from, prep_to, ingredients_inc, ingredients_exc, page, sort_by, sort_order, recipes_per_meal)
	# print("query:\n", query) # XXX DEBUG XXX
	cursor = getCursor()
	cursor.execute(query)
	result = cursor.fetchall()
	return result

def apiSearchRecipes(request):
	result_orig = fetchRecipies("SearchRecipes", request, -1)
	result = fetchRecipies("SearchRecipes", request, 1)
	for row in result:
		row["prep_time"] = str(row["prep_time"])
	data = {"results": len(result_orig), "items": result}
	# print("data:\n", data) # XXX DEBUG XXX
	return jsonApi(200, data)

def getSortBy(param):
	if param == "prep":
		param += "_time"
	if param == "cal":
		param += "ories"
	return param

def recipe_query(name_string, diet_string, prep_time_lower_bound, prep_time_upper_bound, ingr_in, ingr_out, page, sort_by, sort_order, recipes_per_meal):
	# print("recipes: ", recipes_per_meal) # XXX DEBUG XXX
	sql_start = "SELECT Recipe.Id AS id, Recipe.Name AS name, Recipe.Prep_Time AS prep_time, Recipe.Calories AS calories, Recipe.Url AS url, Recipe.Image AS image \nFROM Recipe "
	if 1 < int(recipes_per_meal):
		sql_start = "SELECT Recipe.Id AS id, Recipe.Name AS name\nFROM Recipe "
	lim_off = "\nLIMIT {0} OFFSET {1}".format(6*int(recipes_per_meal), int(page)*6*int(recipes_per_meal))
	if int(recipes_per_meal) < 0:
		lim_off = ""
	sort = "\nORDER BY {0} {1}".format(sort_by, sort_order)
	# Conditions
	first_condition = True
	if name_string != "":
		sql_condition = "\nWHERE LOWER(Recipe.Name) LIKE LOWER('{0}%')".format(name_string)
		first_condition = False
	if diet_string != "any":
		sql_start += ", Diet, Recipe_Diet "
		diet_conds = "Recipe.Id = Recipe_Diet.Recipe_Id and Recipe_Diet.Diet_Id = Diet.Id and Diet.Name = '{0}'\n".format(diet_string)
		if first_condition:
			sql_condition = "\nWHERE {0}".format(diet_conds)
			first_condition = False
		else:
			sql_condition += " and {0}".format(diet_conds)
	if prep_time_lower_bound != "0":
		prep_lower_conds = " Recipe.Prep_Time >= {0} ".format(prep_time_lower_bound)
		if first_condition:
			sql_condition = "\nWHERE {0}".format(prep_lower_conds)
			first_condition = False
		else:
			sql_condition += " and {0}".format(prep_lower_conds)
	if prep_time_upper_bound != "180":
		prep_upper_conds = " Recipe.Prep_Time <= {0} ".format(prep_time_upper_bound)
		if first_condition:
			sql_condition = "\nWHERE {0}".format(prep_upper_conds)
			first_condition = False
		else:
			sql_condition += " and {0}".format(prep_upper_conds)
	if ingr_in != [""]:
		ingr_in_conds = ""
		for ing in ingr_in:
			ingr_in_conds += "and Recipe.Id = ANY(SELECT Recipe.Id FROM Recipe, Recipe_Ingredient, Ingredient WHERE Recipe.Id = Recipe_Ingredient.Recipe_Id and Recipe_Ingredient.Ingredient_Id = Ingredient.Id and LOWER(Ingredient.Name) LIKE LOWER('{0}%'))".format(ing)
		if first_condition:
			sql_condition = "\nWHERE {0}".format(ingr_in_conds[4:])
			first_condition = False
		else:
			sql_condition += " {0}".format(ingr_in_conds)
	if ingr_out != [""]:
		sub_query = ""
		for ing in ingr_out:
			sub_query += " or LOWER(Ingredient.Name) LIKE LOWER('{0}%')".format(ing)
		ingr_out_conds = "Recipe.Id <> ALL(SELECT Recipe.Id FROM Recipe, Recipe_Ingredient, Ingredient WHERE Recipe.Id = Recipe_Ingredient.Recipe_Id and Recipe_Ingredient.Ingredient_Id = Ingredient.Id and ({0}))".format(sub_query[4:])
		if first_condition:
			sql_condition = "\nWHERE {0}".format(ingr_out_conds)
			first_condition = False
		else:
			sql_condition += " \nand {0}".format(ingr_out_conds)
	if first_condition:
		return sql_start + sort + lim_off
	if 0 < int(page):
		return sql_start + sql_condition + sort + lim_off
	return sql_start + sql_condition + sort + lim_off
