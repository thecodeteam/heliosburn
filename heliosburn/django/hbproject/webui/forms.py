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


class RuleForm(forms.Form):
    rule_choices = (('request', 'Request'), ('response', 'Response'))

    name = forms.CharField(label='Name', max_length=100)
    description = forms.CharField(label='Description', widget=forms.Textarea, required=False)
    ruleType = forms.ChoiceField(label='Rule type', choices=rule_choices)


class RuleRequestForm(forms.Form):
    method_choices = (
        ('', 'Select a method'),
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('OPTIONS', 'OPTIONS'),
        ('HEAD', 'HEAD'),
        ('PATCH', 'PATCH'),
        ('CONNECT', 'CONNECT'),
        ('TRACE', 'TRACE'),
    )

    action_type_choices = (
        ('modify_request', 'Modify the request'),
        ('new_response', 'Respond on behalf'),
        ('drop_connection', 'Drop connection'),
        ('delay', 'Delay'),
    )

    filterProtocol = forms.CharField(label='HTTP Protocol', max_length=100,
                                     help_text='HTTP protocol used in the connection. The most commonly used HTTP protocol nowadays is <strong>HTTP/1.1</strong>. Leave this field empty if you are unsure of its purpose.',
                                     required=False)
    filterMethod = forms.ChoiceField(label='HTTP Method', choices=method_choices,
                                     help_text='HTTP methods to indicate the desired action to be performed on the identified resource.',
                                     required=False)
    filterUrl = forms.CharField(label='URL', max_length=200, required=False)

    actionType = forms.ChoiceField(label='Type', choices=action_type_choices)
    actionProtocol = forms.CharField(label='HTTP Protocol', max_length=100, required=False)
    actionMethod = forms.ChoiceField(label='HTTP Method', choices=method_choices, required=False)
    actionUrl = forms.CharField(label='URL', max_length=200, required=False)
    actionStatusCode = forms.CharField(label='Status code', max_length=200, required=False)
    actionStatusDescription = forms.CharField(label='Status description', max_length=200, required=False)
    actionPayload = forms.CharField(label='Payload', widget=forms.Textarea, required=False)
