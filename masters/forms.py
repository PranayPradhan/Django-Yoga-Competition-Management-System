# masters/forms.py
from django import forms
# from .models import Gender

# class GenderForm(forms.ModelForm):
#     class Meta:
#         model = Gender
#         fields = ['name']

#     def clean_name(self):
#         name = self.cleaned_data['name'].strip()
#         if not name:
#             raise forms.ValidationError("Name cannot be empty")
#         return name
