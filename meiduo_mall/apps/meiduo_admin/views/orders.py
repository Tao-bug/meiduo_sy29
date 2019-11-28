from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.orders.models import OrderInfo
from apps.meiduo_admin.serializers.orders import OrderSerializer, OrderDetailSerializer
from apps.meiduo_admin.utils.meiduo_pagination import MeiduoPagination


# 订单
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

    # 修改订单状态
    @action(methods=['PUT'], detail=True)
    def status(self, request, pk):
        # 接收
        order_status = request.data.get('status')

        # 验证
        if not all([order_status]):
            return Response({'error': '参数不完整'}, status=400)

        # 处理
        # 查询订单对象
        # order = OrderInfo.objects.get(pk=pk)
        instance = self.get_object()

        # 修改订单状态
        instance.status = order_status
        instance.save()

        # 响应
        return Response({
            'order_id': instance.order_id,
            'status': order_status
        })
