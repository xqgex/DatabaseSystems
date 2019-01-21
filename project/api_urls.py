# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from project.api import *

urlpatterns = [
	url(r"^get_diets/", apiGetDiets, name="api_get_diets"),
	url(r"^get_ingredients_suggestion/", apiIngredientsSuggestion, name="api_get_ingredients_suggestion"),
	url(r"^get_ingredients/", apiIngredients, name="api_get_ingredients"),
	url(r"^get_recipes_suggestion/", apiRecipesSuggestion, name="api_get_recipes_suggestion"),
	url(r"^search_recipes/", apiSearchRecipes, name="api_search_recipes"),
]
