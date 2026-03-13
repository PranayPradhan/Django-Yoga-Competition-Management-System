from django.urls import path
from . import views

app_name = "masters"

urlpatterns = [
    path("", views.master_index, name="master_index"),
    path("<str:model_name>/", views.master_list, name="master_list"),
    path("<str:model_name>/add/", views.master_add, name="master_add"),
    path("<str:model_name>/<int:pk>/edit/", views.master_edit, name="master_edit"),
]
