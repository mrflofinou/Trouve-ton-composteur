from django.urls import re_path

from . import views

app_name = "composteur"

urlpatterns = [
    re_path(r'^$', views.map, name="map")
]