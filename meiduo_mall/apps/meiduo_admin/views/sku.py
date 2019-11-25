from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.serializers.sku import SkuSerializer
from apps.meiduo_admin.utils.meiduo_pagination import MeiduoPagination
from apps.goods.models import SKU


# sku
class SkuViewSet(ModelViewSet):
    # queryset = SKU.objects.all().order_by('-id')
    def get_queryset(self):
        queryset = SKU.objects
        # 接收查询参数中的关键字
        keyword = self.request.query_params.get('keyword')
        if keyword:
            # 构造查询条件
            # 两个条件为逻辑与关系
            # queryset = queryset.filter(name__contains=keyword, caption__contains=keyword)
            # 两个条件为逻辑或关系
            queryset = queryset.filter(Q(name__contains=keyword) | Q(caption__contains=keyword))
        # 排序
        queryset = queryset.order_by('-id')
        # 返回查询集
        return queryset
    serializer_class = SkuSerializer
    pagination_class = MeiduoPagination
