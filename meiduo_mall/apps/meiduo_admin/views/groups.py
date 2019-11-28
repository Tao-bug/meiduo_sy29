from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, DjangoObjectPermissions
from apps.meiduo_admin.serializers.groups import GroupSerializer
from apps.meiduo_admin.utils.meiduo_pagination import MeiduoPagination


# 组
class GroupViewSet(ModelViewSet):
    permission_classes = [IsAdminUser, DjangoObjectPermissions]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = MeiduoPagination

    # 查询所有组，返回后供添加管理员时选择
    @action(methods=['GET'], detail=False)
    def simple(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
