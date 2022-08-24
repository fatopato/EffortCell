from django import forms
from django.forms import ModelForm

from .models import Iteration


class DateInput(forms.DateInput):
    input_type = 'date'


class IterationForm(ModelForm):

    class Meta:
        model = Iteration
        fields = ['title', 'start_date', 'end_date']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'user': forms.HiddenInput(),
        }
