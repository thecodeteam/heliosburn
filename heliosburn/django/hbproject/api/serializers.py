from rest_framework import serializers
from api.models import User, HttpRequest, HttpRequestHeaders, HttpResponse, HttpResponseHeaders, HttpHeader
from api.models import Session, SessionTraffic, TestPlan, Rule, Filter, FilterHeaders, Action
from api.models import ActionResponse, ActionRequest, ActionHeaders, Match, Recording, RecordingTraffic

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    created_at = serializers.DateTimeField()
    update_at = serializers.DateTimeField()

    def create(self, validated_data):
        return User(**validated_data)

    def update(self, instance, validated_data):
        pass


class HttpRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    http_protocol = serializers.CharField()
    method = serializers.CharField()
    url = serializers.CharField()
    response = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class HttpRequestHeadersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    request = serializers.IntegerField()
    header = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class HttpResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    http_protocol = serializers.CharField()
    status_code = serializers.IntegerField()
    status_description = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class HttpResponseHeadersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    response = serializers.IntegerField()
    header = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class HttpHeaderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    key = serializers.CharField()
    value = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class SessionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    test_plan = serializers.IntegerField()
    user = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    started_at = serializers.DateTimeField()
    stopped_at = serializers.DateTimeField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class SessionTrafficSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    session = serializers.IntegerField()
    http_request = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class TestPlanSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    latency_enabled = serializers.BooleanField()
    client_latency = serializers.IntegerField()
    server_latency = serializers.IntegerField()
    # 'rules' relationship TODO

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RuleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    rule_type = serializers.CharField()
    # 'filters' relationship TODO
    # 'actions' relationsihp TODO
    test_plan = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class FilterSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    method = serializers.CharField()
    status_code = serializers.CharField()
    url = serializers.CharField()
    protocol = serializers.CharField()
    rule = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class FilterHeadersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    filter = serializers.IntegerField()
    header = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField()
    rule = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ActionResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    http_protocol = serializers.CharField()
    status_code = serializers.IntegerField()
    status_description = serializers.CharField()
    payload = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ActionRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    http_protocol = serializers.CharField()
    method = serializers.CharField()
    url = serializers.CharField()
    payload = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ActionHeadersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.IntegerField()
    header = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class MatchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    session = serializers.IntegerField()
    rule = serializers.IntegerField()
    http_request = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RecordingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    user = serializers.IntegerField()
    created_at = serializers.DateTimeField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RecordingTrafficSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    recording = serializers.IntegerField()
    http_request = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


