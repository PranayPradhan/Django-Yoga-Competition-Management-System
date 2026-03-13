from django.urls import path
from . import views

app_name = "dataentry"

urlpatterns = [
    path("", views.index, name="index"),
    path("yoga/", views.bib_verify, {"entry_type": "yoga"}, name="yoga"),
    path("coc/", views.bib_verify, {"entry_type": "coc"}, name="coc"),
    path("score/", views.score_entry, name="score"),
]
