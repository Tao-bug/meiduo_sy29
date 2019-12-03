from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.serializers.spu import SpuSimpleSerializer, SpuSerializer, BrandsSimpleSerialiazer
from apps.goods.models import SPU, Brand
from apps.meiduo_admin.utils.meiduo_pagination import MeiduoPagination


class SpuSimpleView(ListAPIView):
    queryset = SPU.objects.all()
    serializer_class = SpuSimpleSerializer


# 查询获取SPU表列表数据
class SpuViewSet(ModelViewSet):
    # queryset = SPU.objects.all()
    def get_queryset(self):
        queryset = SPU.objects
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
    serializer_class = SpuSerializer
    pagination_class = MeiduoPagination

    # 保存SPU数据
    # def create(self, request, *args, **kwargs):
    #
    #     return


# 简单品牌信息
class BrandsSimpleView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandsSimpleSerialiazer

