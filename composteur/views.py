from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    """ Home page """
    return render(request, "composteur/index.html")

def map(request):
    """ Page to display the results on a google map """
    return render(request, "composteur/map.html")