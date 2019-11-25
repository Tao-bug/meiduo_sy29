import re

from django.http import HttpResponseForbidden
from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'email', 'password']

        # 只读字段
        read_only_field = ['id']
        # 设置密码只写
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    # 验证方法
    def validated_username(self, value):
        # # 接受参数
        #
        # # 判断用户名是否是5-20个字符
        # if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
        #     return HttpResponseForbidden('请输入5-20个字符的用户名')
        # # 判断密码是否是8-20个数字
        # if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
        #     return HttpResponseForbidden('请输入8-20位的密码')
        # # 判断两次密码是否一致
        # if password != password2:
        #     return HttpResponseForbidden('两次输入的密码不一致')
        # # 判断手机号是否合法
        # if not re.match(r'^1[3-9]\d{9}$', mobile):
        #     return HttpResponseForbidden('请输入正确的手机号码')
        # # 校验邮箱
        # if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        #     return HttpResponseForbidden('参数email有误')
        return value

    # 重写创建用户---密码需要加密保存--validated_data验证后的数据
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


