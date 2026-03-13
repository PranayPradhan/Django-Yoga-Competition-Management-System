from django.urls import path
from . import views

app_name = "setting"

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/", views.edit, name="edit"),
]

