from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.models import User
from datetime import date, timedelta
from apps.goods.models import GoodsVisitCount
from rest_framework.generics import ListAPIView
from apps.meiduo_admin.serializers import statistical


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
        # oders.models中增加related_name='orders'
        # 条件：今天下单用户量统计  distinct()-->去重
        # count = User.objects.filter(orders__create_time__gte=today, is_staff=False).count()
        count = User.objects.filter(orders__create_time__gte=today, is_staff=False).distinct().count()
        return Response({
            'count': count,
            'date': today
        })


# 月增用户统计
class MonthView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 月增用户统计
        # 说明 统计过去30 天的用户数
        count_list = []  # [{},{}]
        today = date.today()

        # for i in range(29, -1, -1):
        for i in range(29):

            date_begin = today - timedelta(days=29 - i)
            date_end = date_begin + timedelta(days=1)
            #
            count = User.objects.filter(is_staff=False, date_joined__gte=date_begin, date_joined__lt=date_end).count()
            count_list.append({
                'count': count,
                'date': date_begin
            })

        return Response(count_list)


# 日分类商品访问量
# class GoodsView(APIView):
#     permission_classes = [IsAdminUser]
#
#     def get(self, request):
#         # 查询表中的数据，返回给客户端
#         today = date.today()
#         queryset = GoodsVisitCount.objects.filter(date=today)
#         visit_list = []
#         # 遍历  将对象转字典
#         for visit in queryset:
#             visit_list.append({
#                 "category": visit.category.name,
#                 "count": visit.count
#             })
#
#         return Response(visit_list)


class GoodsView(ListAPIView):
    queryset = GoodsVisitCount.objects.filter(date=date.today())
    serializer_class = statistical.VisitSerializer
