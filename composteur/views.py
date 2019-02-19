from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    """ Home page """
    return render(request, "composteur/index.html")
