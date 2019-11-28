from rest_framework.generics import ListAPIView
from apps.meiduo_admin.serializers.permission import PermissionSerializer
from django.contrib.auth.models import Permission
from apps.meiduo_admin.utils.meiduo_pagination import MeiduoPagination


# 权限
class PermissionView(ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    pagination_class = MeiduoPagination
