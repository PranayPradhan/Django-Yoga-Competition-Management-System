from django import forms
from .models import Participant

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.instance_pk = kwargs.get("instance").pk if kwargs.get("instance") else None
        super().__init__(*args, **kwargs)

    def clean_bib_no(self):
        bib_no = self.cleaned_data["bib_no"]
        qs = Participant.objects.filter(bib_no=bib_no)
        if self.instance_pk:
            qs = qs.exclude(pk=self.instance_pk)
        if qs.exists():
            raise forms.ValidationError("Bib No must be unique")
        return bib_no
