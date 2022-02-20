from xml.dom import ValidationErr
from django import forms

class CalForm(forms.Form):
    x     = forms.IntegerField()
    y     = forms.IntegerField()

    def clean_y(self):
        if self.cleaned_data['y'] == 0:
            raise forms.ValidationError("can't be zero")

        return self.cleaned_data['y']