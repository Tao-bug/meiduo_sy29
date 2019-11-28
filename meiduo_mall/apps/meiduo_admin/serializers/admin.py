from rest_framework import serializers
from apps.users.models import User


# 获取管理员用户列表数据
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile']
