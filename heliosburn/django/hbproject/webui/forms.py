from django import forms
from django.core.validators import MinValueValidator


class LoginForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    rememberLogin = forms.BooleanField(label='Remember me', required=False)


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
        ('modify', 'Modify the request'),
        ('newResponse', 'Respond on behalf'),
        ('drop', 'Drop connection'),
        ('reset', 'Reset connection'),
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

    def clean(self):
        cleaned_data = super(RuleRequestForm, self).clean()
        rule = self._post_data_to_rule(cleaned_data)
        return rule

    def _post_data_to_rule(self, cleaned_data):
        rule = {'ruleType': 'request', 'filter': {}, 'action': {}}

        # Filter Protocol
        rule['filter']['httpProtocol'] = cleaned_data['filterProtocol']

        # Filter Method
        rule['filter']['method'] = cleaned_data['filterMethod']

        # Filter URL
        rule['filter']['url'] = cleaned_data['filterUrl']

        # Get Filter Headers
        rule['filter']['headers'] = []
        filter_header_keys = self.data.getlist('filterHeaderKeys[]')
        filter_header_values = self.data.getlist('filterHeaderValues[]')
        if filter_header_keys:
            for index, key in enumerate(filter_header_keys):
                value = filter_header_values[index]
                rule['filter']['headers'].append({'key': key, 'value': value})

        # Action
        # Action type
        rule['action']['type'] = cleaned_data['actionType']

        if cleaned_data['actionType'] == 'drop' or cleaned_data['actionType'] == 'reset':
            return rule

        if cleaned_data['actionType'] == 'modify':
            rule['action']['httpProtocol'] = cleaned_data['actionProtocol']
            rule['action']['method'] = cleaned_data['actionMethod']
            rule['action']['url'] = cleaned_data['actionUrl']

        if cleaned_data['actionType'] == 'newResponse':
            rule['action']['httpProtocol'] = cleaned_data['actionProtocol']
            rule['action']['statusCode'] = cleaned_data['actionStatusCode']
            rule['action']['statusDescription'] = cleaned_data['actionStatusDescription']
            rule['action']['payload'] = cleaned_data['actionPayload']

        # Get Action Headers
        rule['action']['headers'] = []
        action_header_keys = self.data.getlist('actionHeaderKeys[]')
        action_header_values = self.data.getlist('actionHeaderValues[]')
        if action_header_keys:
            for index, key in enumerate(action_header_keys):
                value = action_header_values[index]
                rule['action']['headers'].append({'key': key, 'value': value})

        return rule
