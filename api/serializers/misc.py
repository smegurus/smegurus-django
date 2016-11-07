from rest_framework import exceptions, serializers


class JudgementSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    comment = serializers.CharField(max_length=2055)


class IntegerSerializer(serializers.Serializer):
    value = serializers.IntegerField()


class BooleanSerializer(serializers.Serializer):
    value = serializers.BooleanField()


class DateTimeSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()


class JSONDictionarySerializer(serializers.Serializer):
    array = serializers.JSONField()
