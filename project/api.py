# -*- coding: utf-8 -*-
import json
from project.views import jsonApi

def apiSuggestion(request):
	if not request.is_ajax():
		return jsonApi(300, "Invalid call")
	data = {"suggestions": [
			{ "value": "United Arab Emirates", "data": "AE" },
			{ "value": "United Kingdom",       "data": "UK" },
			{ "value": "United States",        "data": "US" }
		]}
	return jsonApi(200, data)
