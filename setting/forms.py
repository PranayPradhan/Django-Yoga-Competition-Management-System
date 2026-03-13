from django import forms
from .models import School

class SettingForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ["yob_min", "yob_max", "yoc"]
