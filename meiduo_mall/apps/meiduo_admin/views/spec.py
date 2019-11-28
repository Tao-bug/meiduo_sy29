from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from apps.goods.models import SPUSpecification
from apps.meiduo_admin.serializers.spec import SpecSerializer, SpecBySpuSerializer
from apps.meiduo_admin.utils.meiduo_pagination import MeiduoPagination
from rest_framework.permissions import IsAdminUser, DjangoObjectPermissions


# 商品规格管理
class SpecViewSet(ModelViewSet):
    # permission_classes = [IsAdminUser, DjangoObjectPermissions]

    queryset = SPUSpecification.objects.all().order_by('-id')
    serializer_class = SpecSerializer
    pagination_class = MeiduoPagination


# sku-根据spu_id查询规格及选项
class SpecBySpuView(ListAPIView):
    # def get(self,request,*args,**kwargs):
    # 根据标准商品编号查询规格及选项
    serializer_class = SpecBySpuSerializer

    # 需要从路径中提取参数，拼接查询条件
    def get_queryset(self):
        # 视图对象的属性kwargs表示从路径中提取的关键字参数
        return SPUSpecification.objects.filter(spu_id=self.kwargs.get('spu_id'))
