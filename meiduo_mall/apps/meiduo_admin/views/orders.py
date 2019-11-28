from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.orders.models import OrderInfo
from apps.meiduo_admin.serializers.orders import OrderSerializer
from apps.meiduo_admin.utils.meiduo_pagination import MeiduoPagination


class OrderViewSet(ReadOnlyModelViewSet):
    # queryset = OrderInfo.objects.all()
    def get_queryset(self):
        queryset = OrderInfo.objects
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(order_id__contains=keyword)
        queryset = queryset.order_by('-create_time')
        return queryset
    serializer_class = OrderSerializer
    pagination_class = MeiduoPagination
