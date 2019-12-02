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
    queryset = SPU.objects.all()
    serializer_class = SpuSerializer
    pagination_class = MeiduoPagination


# 简单品牌信息
class BrandsSimpleView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandsSimpleSerialiazer

