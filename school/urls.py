# school/urls.py
from django.urls import path
from . import views

app_name = "school"

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add_school, name="add"),
    path("<int:pk>/edit/", views.edit_school, name="edit"),
    path("edit_index/", views.edit_index, name="edit_index"),
]
