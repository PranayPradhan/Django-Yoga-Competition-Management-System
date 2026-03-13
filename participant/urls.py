"""
participant - URL configuration

"""
from django.urls import path
from . import views

app_name = "participant"

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("<int:pk>/edit/", views.edit, name="edit"),
    path("edit_index/", views.edit_index, name="edit_index"),
]
