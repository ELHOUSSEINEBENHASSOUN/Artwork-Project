from django import forms
from Artwork.models import *


class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = "__all__"
        # exclude = ["proprietaire"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (element, field) in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class Html5DateInput(forms.DateInput):
    input_type = 'date'


class Html5TimeInput(forms.TimeInput):
    input_type = 'time'


class DemandeForm(forms.ModelForm):
    class Meta:
        model = DemandePret
        fields = "__all__"
        widgets = {
            'date_debut': Html5DateInput(),
            'date_fin': Html5DateInput(),
            'h_debut': Html5TimeInput(),
            'h_fin': Html5TimeInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (element, field) in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
