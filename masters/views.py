from django.shortcuts import render, redirect, get_object_or_404
from .registry import get_master_models

def master_index(request):
    masters = []

    for slug, model in get_master_models().items():
        masters.append({
            "slug": slug,
            "title": model._meta.verbose_name_plural.title()
        })

    return render(request, "masters/master_index.html", {
        "masters": masters
    })

def master_list(request, model_name):
    masters = get_master_models()

    if model_name not in masters:
        raise Http404("Invalid master table")

    model = masters[model_name]

    records = model.objects.all()

    return render(request, "masters/master_list.html", {
        "title": model._meta.verbose_name_plural.title(),
        "records": records,
        "model_name": model_name
    })

from django.forms import modelform_factory

def master_add(request, model_name):
    masters = get_master_models()
    model = masters.get(model_name)

    if not model:
        raise Http404("Invalid master table")

    Form = modelform_factory(model, fields=["name"])

    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect("masters:master_list", model_name=model_name)
    else:
        form = Form()

    return render(request, "masters/master_form.html", {
        "form": form,
        "title": f"Add {model._meta.verbose_name}"
    })

def master_edit(request, model_name, pk):
    masters = get_master_models()
    model = masters.get(model_name)

    if not model:
        raise Http404("Invalid master table")

    obj = get_object_or_404(model, pk=pk)
    Form = modelform_factory(model, fields=["name"])

    if request.method == "POST":
        form = Form(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("masters:master_list", model_name=model_name)
    else:
        form = Form(instance=obj)

    return render(request, "masters/master_form.html", {
        "form": form,
        "title": f"Edit {model._meta.verbose_name}"
    })
