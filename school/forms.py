# school/forms.py
from django import forms
from .models import School

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ["name", "code", "contact", "tic", "tic_no"]

    def __init__(self, *args, **kwargs):
        self.instance_pk = kwargs.get("instance").pk if kwargs.get("instance") else None
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data["code"]

        qs = School.objects.filter(code=code)
        if self.instance_pk:
            qs = qs.exclude(pk=self.instance_pk)

        if qs.exists():
            raise forms.ValidationError("Code field must be unique")

        return code
