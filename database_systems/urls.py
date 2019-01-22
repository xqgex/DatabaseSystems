"""database_systems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r"^$", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r"^$", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r"^blog/", include("blog.urls"))
"""
from django.conf.urls import include, url, handler404, handler500
from django.contrib import admin
from project.views import HomePageView
admin.autodiscover()

handler404 = "project.views.handler404"
handler500 = "project.views.handler500"

urlpatterns = [
	url(r"^$", HomePageView.as_view(), name="home"),
	url(r"^api/", include("project.api_urls")),
	url(r"^admin/", admin.site.urls),
]
