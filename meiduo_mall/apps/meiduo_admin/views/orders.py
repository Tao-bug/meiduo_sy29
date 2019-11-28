from rest_framework.viewsets import ModelViewSet
from apps.orders.models import OrderInfo
from apps.meiduo_admin.serializers.orders import OrderSerializer
from apps.meiduo_admin.utils.meiduo_pagination import MeiduoPagination


class OrderViewSet(ModelViewSet):
    queryset = OrderInfo.objects.all()
    serializer_class = OrderSerializer
    pagination_class = MeiduoPagination
