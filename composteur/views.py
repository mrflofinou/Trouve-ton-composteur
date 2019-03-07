from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .forms import SignUpForm
from .libs.google_map_API import GoogleApiRequest
from .libs.api_keys import google_apis

def index(request):
    """ Home page """
    return render(request, "composteur/index.html")

def map(request):
    """ Page to display the results on a google map """

    query = request.GET.get("query")
    google_request = GoogleApiRequest(query)
    lat, lng = google_request.get_coordinates()
    javascript_api = google_apis["JAVASCRIPT_API"]
    context = {
        "query" : query,
        "lat" : str(lat),
        "lng" : str(lng),
        "js_api" : javascript_api
    }
    return render(request, "composteur/map.html", context)

def signup(request):
    """ Page to signup """

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            
            # logger.info('New user registered', exc_info=True, extra={
            #     # Optionally pass a request and we'll grab any information we can
            #     'request': request,
            # })

            return redirect("index")
    else:
        form = SignUpForm()
    context = {"form": form}
    return render(request, "composteur/signup.html", context)