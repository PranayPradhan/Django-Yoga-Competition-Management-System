from django.shortcuts import render, redirect, get_object_or_404
from .models import Participant
from .forms import ParticipantForm

def index(request):
    participants = Participant.objects.select_related(
        "school", "age_cat", "gender", "yoga_sub_cat",
        "standard", "sec", "diet"
    ).order_by("name")

    return render(request, "participant/index.html", {
        "participants": participants,
        "is_edit": False,
    })


def edit_index(request):
    participants = Participant.objects.select_related(
        "school", "age_cat", "gender", "yoga_sub_cat",
        "standard", "sec", "diet"
    ).order_by("name")

    return render(request, "participant/index.html", {
        "participants": participants,
        "is_edit": True,
    })


def add(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("participant:index")
    else:
        form = ParticipantForm()

    return render(request, "participant/form.html", {
        "form": form,
        "title": "Add Participant",
    })

def edit(request, pk):
    participant = get_object_or_404(Participant, pk=pk)

    if request.method == "POST":
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect("participant:index")
    else:
        form = ParticipantForm(instance=participant)

    return render(request, "participant/form.html", {
        "form": form,
        "title": "Edit Participant",
    })
