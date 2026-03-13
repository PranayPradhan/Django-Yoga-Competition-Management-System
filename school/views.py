# school/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import School
from .forms import SchoolForm
from django.http import HttpResponse

# Create your views here.

def index(request):
    # return HttpResponse("Reached school app index")   
    schools = School.objects.all().order_by("name")
    return render(request, "school/index.html", {
        "schools": schools
    })

def edit_index(request):
    # return HttpResponse("Reached school app edit_index")   
    schools = School.objects.all().order_by("name")
    return render(request, "school/index.html", {
        "schools": schools,
        "is_edit": True,
    })


def add_school(request):
    if request.method == "POST":
        form = SchoolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("school:index")
    else:
        form = SchoolForm()

    return render(request, "school/form.html", {
        "form": form,
        "title": "Add School",
        "is_edit": False,
    })


def edit_school(request, pk):
    school = get_object_or_404(School, pk=pk)

    if request.method == "POST":
        form = SchoolForm(request.POST, instance=school)
        if form.is_valid():
            form.save()
            return redirect("school:index")
    else:
        form = SchoolForm(instance=school)

    return render(request, "school/form.html", {
        "form": form,
        "title": "Edit School",
        "is_edit": True,
    })
