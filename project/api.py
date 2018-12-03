# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from project.views import HomePageView

urlpatterns = [
	url(r"^get_list/", HomePageView.as_view(), name="api_get_list"),
]
