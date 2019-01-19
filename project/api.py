# -*- coding: utf-8 -*-
import json
from project.views import jsonApi

def apiGetDiets(request):
	data = {"list": [
			{"name": "balanced",		"desc": "Protein/Fat/Carb values in 15/35/50 ratio"},
			{"name": "high-protein",	"desc": "More then 50% of total calories from proteins"},
			{"name": "alcohol-free",	"desc": "No alcohol used or contained"}
		]}
	return jsonApi(200, data)

def apiIngredientsSuggestion(request):
	if not request.is_ajax():
		return jsonApi(300, "Invalid call")
	data = {"suggestions": [
			{"name": "Apple"},
			{"name": "Lemon"},
			{"name": "Milk"}
		]}
	return jsonApi(200, data)

def apiRecipesSuggestion(request):
	if not request.is_ajax():
		return jsonApi(300, "Invalid call")
	data = {"suggestions": [
			{"name": "Hot Apple Pie",			"calories": "289"},
			{"name": "Sparkling Apple Cocktail recioes",	"calories": "609"},
			{"name": "Apple-Lemon-Ginger Juice",		"calories": "254"}
		]}
	return jsonApi(200, data)
