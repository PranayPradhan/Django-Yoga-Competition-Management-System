from django.apps import apps
from .models import MasterBase

def get_master_models():
    masters = {}

    for model in apps.get_models():
        if issubclass(model, MasterBase) and not model._meta.abstract:
            slug = model.__name__.lower().replace("category", "_category")
            masters[slug] = model

    return masters
