from django.shortcuts import render
from django.http import HttpResponse

from .libs.google_map_API import GoogleApiRequest

def index(request):
    """ Home page """
    return render(request, "composteur/index.html")

def map(request):
    """ Page to display the results on a google map """

    query = request.GET.get("query")
    google_request = GoogleApiRequest(query)
    lat, lng = google_request.get_coordinates()
    context = {
        "query" : query,
        "lat" : str(lat),
        "lng" : str(lng)
    }
    return render(request, "composteur/map.html", context)