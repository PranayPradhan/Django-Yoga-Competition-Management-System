from django.shortcuts import render, redirect
from .models import School
from .forms import SettingForm

def index(request):
    setting = School.objects.first()
    return render(request, "setting/index.html", {"setting": setting})

def edit(request):
    setting, _ = School.objects.get_or_create(pk=1)

    if request.method == "POST":
        form = SettingForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()
            return redirect("setting:index")
    else:
        form = SettingForm(instance=setting)

    return render(request, "setting/form.html", {"form": form})
