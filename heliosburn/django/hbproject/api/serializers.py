from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    created_at = serializers.DateTimeField()
    update_at = serializers.DateTimeField()


class HttpRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    http_protocol = serializers.CharField()
    method = serializers.CharField()
    url = serializers.CharField()
    response = serializers.CharField()


class HttpRequestHeadersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    request = serializers.IntegerField()
    header = serializers.IntegerField()


class HttpResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    http_protocol = serializers.CharField()
    status_code = serializers.IntegerField()
    status_description = serializers.CharField()


class HttpResponseHeadersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    response = serializers.IntegerField()
    header = serializers.IntegerField()


class HttpHeaderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    key = serializers.CharField()
    value = serializers.CharField()


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


class SessionTrafficSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    session = serializers.IntegerField()
    http_request = serializers.IntegerField()


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


class RuleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    rule_type = serializers.CharField()
    # 'filters' relationship TODO
    # 'actions' relationsihp TODO
    test_plan = serializers.IntegerField()


class FilterSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    method = serializers.CharField()
    status_code = serializers.CharField()
    url = serializers.CharField()
    protocol = serializers.CharField()
    rule = serializers.IntegerField()


class FilterHeadersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    filter = serializers.IntegerField()
    header = serializers.IntegerField()


class ActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField()
    rule = serializers.IntegerField()


class ActionResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    http_protocol = serializers.CharField()
    status_code = serializers.IntegerField()
    status_description = serializers.CharField()
    payload = serializers.CharField()


class ActionRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    http_protocol = serializers.CharField()
    method = serializers.CharField()
    url = serializers.CharField()
    payload = serializers.CharField()


class ActionHeadersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.IntegerField()
    header = serializers.IntegerField()


class MatchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    session = serializers.IntegerField()
    rule = serializers.IntegerField()
    http_request = serializers.IntegerField()


class RecordingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    user = serializers.IntegerField()
    created_at = serializers.DateTimeField()


class RecordingTrafficSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    recording = serializers.IntegerField()
    http_request = serializers.IntegerField()


