from rest_framework import exceptions, serializers


class JudgementSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    comment = serializers.CharField(max_length=2055)


class IntegerSerializer(serializers.Serializer):
    value = serializers.IntegerField()
