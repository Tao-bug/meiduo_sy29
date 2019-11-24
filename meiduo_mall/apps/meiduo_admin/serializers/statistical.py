from rest_framework import serializers


class VisitSerializer(serializers.Serializer):
    category = serializers.StringRelatedField(read_only=True)
    count = serializers.IntegerField()