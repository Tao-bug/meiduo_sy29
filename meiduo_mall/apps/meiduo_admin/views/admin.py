from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from apps.users.models import User
import jwt
from datetime import datetime, timedelta
from apps.meiduo_admin.Mixin import TokenValidateMixin
from rest_framework_jwt.utils import jwt_payload_handler
from apps.meiduo_admin.serializers.admin import AdminSerializer
from apps.meiduo_admin.utils.meiduo_pagination import MeiduoPagination


class LoginView(APIView):
    def post(self, request):
        # 接收数据
        json_dict = request.data

        # 验证
        try:
            user = User.objects.get(username=json_dict.get('username'), is_staff=True)
        except:
            return JsonResponse({'error': '用户不存在'}, status=400)

        if not user.check_password(json_dict.get('password')):
            return JsonResponse({'error': '密码有误'}, status=400)

        # 状态保存
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(weeks=2)
        }
        token = jwt.encode(payload, settings.SECRET_KEY)

        # 响应
        return Response({
            "username": user.username,
            "id": user.id,
            "token": token
        })


class TestView(TokenValidateMixin, APIView):
    def get(self, request):
        # 验证　封装
        # token = request.META.get('HTTP_AUTHORIZATION')[4:]
        # try:
        #     payload = jwt.decode(token, settings.SECRET_KEY)
        # except:
        #     pass

        return Response({'msg': 'ok'})


# jwt --- token  自定义响应体
def meiduo_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'id': user.id,
        'username': user.username
    }


# 自定义载荷
def meiduo_payload_handler(user):
    payload = jwt_payload_handler(user)
    # 去掉email
    del payload['email']

    # 增加mobile
    payload['mobile'] = user.mobile

    return payload


# 获取管理员用户列表数据
class AdminViewSet(ModelViewSet):
    queryset = User.objects.filter(is_staff=True).order_by('-id')
    serializer_class = AdminSerializer
    pagination_class = MeiduoPagination

