# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import textwrap
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.http import JsonResponse

class HomePageView(TemplateView):
	template_name = "index.html"

def jsonApi(status, message, code=200):
	return JsonResponse(data={"status": status, "message": message}, status=code)

def handler404(request):
	return jsonApi(404, "Error 404")

def handler500(request):
	return jsonApi(500, "Error 500")

#class HomePageView_2(View):
#	def dispatch(request, *args, **kwargs):
#		response_text = textwrap.dedent("""\
#			<html>
#			<head>
#			<title>Greetings to the world</title>
#			</head>
#			<body>
#			<h1>Greetings to the world</h1>
#			<p>Hello, world!</p>
#			</body>
#			</html>""")
#		return HttpResponse(response_text)
