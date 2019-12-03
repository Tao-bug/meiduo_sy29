from rest_framework.viewsets import ModelViewSet
from apps.goods.models import Brand
from apps.meiduo_admin.serializers.brands import BrandSerializer
from apps.meiduo_admin.utils.meiduo_pagination import MeiduoPagination


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.order_by('-id')
    serializer_class = BrandSerializer
    pagination_class = MeiduoPagination