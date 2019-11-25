from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SPUSpecification
from apps.meiduo_admin.serializers.spec import SpecSerializer
from apps.meiduo_admin.utils.meiduo_pagination import MeiduoPagination


# 商品规格管理
class SpecViewSet(ModelViewSet):
    queryset = SPUSpecification.objects.all()
    serializer_class = SpecSerializer
    pagination_class = MeiduoPagination
