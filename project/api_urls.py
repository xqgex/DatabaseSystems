# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from project.api import apiSuggestion

urlpatterns = [
	url(r"^get_list/", apiSuggestion, name="api_get_list"),
]
