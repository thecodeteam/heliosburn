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


class RuleRequestForm(forms.Form):
    filterProtocol = forms.CharField(label='HTTP Protocol', max_length=100)
    filterMethod = forms.ChoiceField(label='HTTP Method', choices=(
        ('', 'Select a method'), ('GET', 'GET'), ('PUT', 'PUT'), ('OPTIONS', 'OPTIONS'), ('HEAD', 'HEAD'), ('POST', 'POST')))
    filterUrl = forms.CharField(label='URL', max_length=200)
    actionType = forms.CharField(label='Type', max_length=200)
    actionProtocol = forms.CharField(label='HTTP Protocol', max_length=100)
    actionMethod = forms.CharField(label='HTTP Method', max_length=200)
    actionUrl = forms.CharField(label='URL', max_length=200)
    actionStatusCode = forms.CharField(label='Status code', max_length=200)
    actionStatusMessage = forms.CharField(label='Status code', max_length=200)
