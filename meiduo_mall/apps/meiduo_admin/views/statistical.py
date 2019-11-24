from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.models import User
from datetime import datetime,date


# 统计总数
class TotalView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):

        # 统计总数
        count = User.objects.filter(is_staff=False).count()
        return Response({
            'count': count,
            'date': date.today()
        })


# 统计今天注册人数
class TodayView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 统计今天注册人数
        today = date.today()
        # 条件：注册时间大于等于今天
        count = User.objects.filter(date_joined__gte=today, is_staff=False).count()
        return Response({
            'count': count,
            'date': today
        })


# 日活跃用户统计
class ActiveView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 日活跃用户统计
        today = date.today()
        # 条件：今天登陆用户
        count = User.objects.filter(last_login__gte=today, is_staff=False).count()
        return Response({
            'count': count,
            'date': today
        })


# 日下单用户量统计
class OrderView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 日活跃用户统计
        today = date.today()
        # 条件：今天下单用户量统计  distinct()-->去重
        count = User.objects.filter(orders__create_time__gte=today, is_staff=False).distinct().count()
        return Response({
            'count': count,
            'date': today
        })

