from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse('<h1>Blog Home page<h1>')


def about(request):
    return HttpResponse('<h1>About Page<h1>')