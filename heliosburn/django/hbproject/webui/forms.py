from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class LoginForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    rememberLogin = forms.BooleanField(label='Remember me', required=False)


class TestPlanForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    description = forms.CharField(label='Description', widget=forms.Textarea)


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

    ruleType = forms.ChoiceField(label='Rule type', choices=(('request', 'Request'), ('response', 'Response')),
                                 required=True)

    filterProtocol = forms.CharField(label='HTTP Protocol', max_length=100,
                                     help_text='HTTP protocol used in the connection. The most commonly used HTTP protocol nowadays is <strong>HTTP/1.1</strong>. Leave this field empty if you are unsure of its purpose.',
                                     required=False)
    filterMethod = forms.ChoiceField(label='HTTP Method', choices=method_choices,
                                     help_text='HTTP methods to indicate the desired action to be performed on the identified resource.',
                                     required=False)
    filterUrl = forms.CharField(label='URL', max_length=200, required=False)
    filterStatusCode = forms.IntegerField(label='Status Code', required=False)

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

    # noinspection PyPep8Naming
    def _post_data_to_rule(self, cleaned_data):
        rule = {'filter': {}, 'action': {}}

        rule['ruleType'] = cleaned_data['ruleType']

        # Filter Protocol
        if cleaned_data['filterProtocol']:
            rule['filter']['httpProtocol'] = cleaned_data['filterProtocol']

        # Filter Method
        if cleaned_data['filterMethod']:
            rule['filter']['method'] = cleaned_data['filterMethod']

        # Filter URL
        if cleaned_data['filterUrl']:
            rule['filter']['url'] = cleaned_data['filterUrl']

        # Get Filter Request Headers
        filter_requestHeader_keys = self.data.getlist('filterRequestHeaderKeys[]')
        filter_requestHeader_values = self.data.getlist('filterRequestHeaderValues[]')
        if filter_requestHeader_keys:
            rule['filter']['requestHeaders'] = []
            for index, key in enumerate(filter_requestHeader_keys):
                if key:
                    value = filter_requestHeader_values[index]
                    rule['filter']['requestHeaders'].append({'key': key, 'value': value})

        if cleaned_data['ruleType'] == 'response':
            # Filter Status Code
            rule['filter']['statusCode'] = cleaned_data['filterStatusCode']

            # Get Filter Response Headers
            filter_responseHeader_keys = self.data.getlist('filterResponseHeaderKeys[]')
            filter_responseHeader_values = self.data.getlist('filterResponseHeaderValues[]')
            if filter_requestHeader_keys:
                rule['filter']['responseHeaders'] = []
                for index, key in enumerate(filter_responseHeader_keys):
                    if key:
                        value = filter_responseHeader_values[index]
                        rule['filter']['responseHeaders'].append({'key': key, 'value': value})


        # Action
        # Action type
        rule['action']['type'] = cleaned_data['actionType']

        if cleaned_data['actionType'] == 'drop' or cleaned_data['actionType'] == 'reset':
            return rule

        if cleaned_data['actionType'] == 'modify':
            if cleaned_data['actionProtocol']:
                rule['action']['httpProtocol'] = cleaned_data['actionProtocol']
            if cleaned_data['actionMethod']:
                rule['action']['method'] = cleaned_data['actionMethod']
            if cleaned_data['actionUrl']:
                rule['action']['url'] = cleaned_data['actionUrl']
            action_header_keys = self.data.getlist('actionHeaderKeys[]')
            action_header_values = self.data.getlist('actionHeaderValues[]')
            if action_header_keys:
                rule['action']['setHeaders'] = []
                for index, key in enumerate(action_header_keys):
                    if key:
                        value = action_header_values[index]
                        rule['action']['setHeaders'].append({'key': key, 'value': value})
            action_deleteHeader_keys = self.data.getlist('actionDeleteHeaderKeys[]')
            if action_deleteHeader_keys:
                rule['action']['deleteHeaders'] = []
                for index, key in enumerate(action_deleteHeader_keys):
                    if key:
                        rule['action']['deleteHeaders'].append({'key': key})

        if cleaned_data['actionType'] == 'newResponse':
            if cleaned_data['actionProtocol']:
                rule['action']['httpProtocol'] = cleaned_data['actionProtocol']
            if cleaned_data['actionStatusCode']:
                rule['action']['statusCode'] = cleaned_data['actionStatusCode']
            if cleaned_data['actionStatusDescription']:
                rule['action']['statusDescription'] = cleaned_data['actionStatusDescription']
            if cleaned_data['actionPayload']:
                rule['action']['payload'] = cleaned_data['actionPayload']
            action_header_keys = self.data.getlist('actionHeaderKeys[]')
            action_header_values = self.data.getlist('actionHeaderValues[]')
            if action_header_keys:
                rule['action']['headers'] = []
                for index, key in enumerate(action_header_keys):
                    if key:
                        value = action_header_values[index]
                        rule['action']['headers'].append({'key': key, 'value': value})

        return rule


class QoSForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    latency = forms.IntegerField(label='Link latency', initial=0,
                                 validators=[MinValueValidator(0)])
    jitterMin = forms.IntegerField(label='Min jitter', initial=0,
                                   validators=[MinValueValidator(0)])
    jitterMax = forms.IntegerField(label='Max jitter', initial=0,
                                   validators=[MinValueValidator(0)])
    trafficLoss = forms.FloatField(label='Traffic loss ratio', initial=0,
                                   validators=[MinValueValidator(0), MaxValueValidator(1)])

    def clean(self):
        cleaned_data = super(QoSForm, self).clean()
        cleaned_data['jitter'] = {}
        cleaned_data['jitter']['min'] = cleaned_data.pop('jitterMin')
        cleaned_data['jitter']['max'] = cleaned_data.pop('jitterMax')
        return cleaned_data


class ServerOverloadForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    description = forms.CharField(label='Description', widget=forms.Textarea)


class RecordingForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    description = forms.CharField(label='Description', widget=forms.Textarea)