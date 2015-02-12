from django import forms
from django.core.validators import MinValueValidator


class TestPlanForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    latencyEnabled = forms.BooleanField(label='Enable latency', required=False)
    clientLatency = forms.IntegerField(label='Client latency', required=False, initial=0,
                                       validators=[MinValueValidator(0)])
    serverLatency = forms.IntegerField(label='Server latency', required=False, initial=0,
                                       validators=[MinValueValidator(0)])

