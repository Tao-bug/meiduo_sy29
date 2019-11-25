from rest_framework.generics import ListAPIView
from apps.meiduo_admin.serializers.category import Category3Serializer
from apps.goods.models import GoodsCategory


# sku-第三级分类
class Category3View(ListAPIView):
    serializer_class = Category3Serializer
    # 第三级分类没有子类
    queryset = GoodsCategory.objects.filter(subs__isnull=True)
