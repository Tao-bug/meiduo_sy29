from rest_framework import serializers
from django.contrib.auth.models import Group


# 组
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
