from rest_framework import serializers
from apps.users.models import User


# 获取管理员用户列表数据
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id', 'username', 'email', 'mobile']
        fields = ['id', 'username', 'email', 'mobile', 'password', 'groups', 'user_permissions']
        read_only_field = ['id']

    # 重写创建--密码需要加密
    def create(self, validated_data):
        instance = super().create(validated_data)

        # 密码加密
        instance.set_password(validated_data.get('password'))
        # 设置管理员
        instance.is_staff = True
        instance.save()

        return instance

    # 重写创建--密码需要加密
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance
