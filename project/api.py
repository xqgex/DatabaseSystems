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

def apiIngredients(request):
	if not request.is_ajax():
		return jsonApi(300, "Invalid call")
	data = {"categories": [
			{
				"name": "Sweets",
				"desc": "Sweet products, Candies and Sugar",
				"list": ["Sweet Ingredients #1", "Sweet Ingredients #2", "Sweet Ingredients #3"]
			}, {
				"name": "Vegetable",
				"desc": "Vegetable and Greens",
				"list": ["Vegetable Ingredients #1", "Vegetable Ingredients #2", "Vegetable Ingredients #3", "Vegetable Ingredients #4"]
			}, {
				"name": "Cooking  & Baking",
				"desc": "Cooking and Baking products - oils, flours…",
				"list": ["Cooking Ingredients #1", "Cooking Ingredients #2"]
			}
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

def apiSearchRecipes(request):
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
