from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.orders.models import OrderInfo
from apps.meiduo_admin.serializers.orders import OrderSerializer, OrderDetailSerializer
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

    # serializer_class = OrderSerializer
    # 需要根据不同的请求，调用不同的序列化器，所以不用属性，改用方法
    def get_serializer_class(self):
        if 'pk' in self.kwargs:
            # 查询一条
            return OrderDetailSerializer
        else:
            # 查询多条
            return OrderSerializer

    pagination_class = MeiduoPagination
