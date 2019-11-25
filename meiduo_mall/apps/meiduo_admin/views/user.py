from rest_framework.generics import ListCreateAPIView
from apps.users.models import User
from apps.meiduo_admin.serializers.user import UserSerializer
from apps.meiduo_admin.utils.meiduo_pagination import MeiduoPagination


class UserView(ListCreateAPIView):
    # queryset = User.objects.filter(is_staff=False, username__contains=request.query_param.get('keyword'))
    def get_queryset(self):
        # self.request  ===> 定一类时没这个属性，而是对象创建后，增加的这个属性
        # 接收参数
        keyword = self.request.query_params.get('keyword')
        # 基础查询
        queryset = User.objects.filter(is_staff=False)
        # 判断  如果有参数，则拼接
        if keyword:
            queryset = queryset.filter(username__contains=keyword)
        # 返回查询
        return queryset

    serializer_class = UserSerializer

    # 分页
    pagination_class = MeiduoPagination

    # 重写  返回结果
    # def get_paginated_response(self, data):
    #     return {
    #
    #     }

