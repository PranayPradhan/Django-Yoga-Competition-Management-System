from django.urls import path
from . import views

app_name = "report"

urlpatterns = [
    path("", views.index, name="index"),
    path("event_mc_call_sheet/<int:pk>", views.event_mc_call_sheet, name="event_mc_call_sheet"),
    path("coc_mc_call_sheet", views.coc_mc_call_sheet, name="coc_mc_call_sheet"),
    path("competition_results", views.competition_results, name="competition_results"),
]
