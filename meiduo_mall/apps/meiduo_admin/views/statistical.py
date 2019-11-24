from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.models import User
from datetime import datetime


class TotalView(APIView):
    def get(self, request):
        permission_classes = [IsAdminUser]

        # 统计总数
        count = User.objects.filter(is_staff=False).count()
        return Response({
            'count': count,
            'date': datetime.today(),
        })
