from django import forms
from django.forms import ModelForm
from bootstrap_modal_forms.forms import BSModalModelForm

from .models import Iteration, Member


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


class MemberForm(BSModalModelForm):
    class Meta:
        model = Member
        fields = ('name', 'role')