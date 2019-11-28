from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group
from apps.meiduo_admin.serializers.groups import GroupSerializer
from apps.meiduo_admin.utils.meiduo_pagination import MeiduoPagination


# 组
class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = MeiduoPagination
