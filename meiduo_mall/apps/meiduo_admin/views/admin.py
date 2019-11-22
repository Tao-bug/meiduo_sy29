from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.models import User
import jwt
from datetime import datetime, timedelta


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

