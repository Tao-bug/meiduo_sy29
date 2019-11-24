import jwt
from django.conf import settings
from rest_framework.response import Response


class TokenValidateMixin(object):
    def dispach(self, request, *args, **kwargs):
        # 验证
        token = request.META.get('HTTP_AUTHORIZATION')[4:]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            return Response({'error': '身份信息无效'}, status=401)

        return super().dispach(request, *args, **kwargs)
