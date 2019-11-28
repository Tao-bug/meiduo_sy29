from rest_framework import serializers
from django.contrib.auth.models import Permission


# 权限
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


# 简单查询
class PermissionSimpleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
