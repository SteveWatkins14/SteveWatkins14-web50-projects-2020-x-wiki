from random import random
from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.redirect_view, name="redirect_view"),
    path("wiki/<str:entry>/", views.get_entry, name="get_entry"),
    path("search/", views.search, name="search"),
    path("random/", views.random_entry, name="random_entry"),
    path("new/", views.new_entry, name="new_entry"),
    path("edit/<str:entry>", views.edit, name="edit"),
]