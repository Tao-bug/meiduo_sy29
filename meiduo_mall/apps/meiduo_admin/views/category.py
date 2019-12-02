from rest_framework.generics import ListAPIView
from apps.meiduo_admin.serializers.category import Category3Serializer, Category1Serializer, CategorySerializer
from apps.goods.models import GoodsCategory


# sku-第三级分类
class Category3View(ListAPIView):
    serializer_class = Category3Serializer
    # 第三级分类没有子类
    queryset = GoodsCategory.objects.filter(subs__isnull=True)


# 获取一级分类信息
class Category1View(ListAPIView):
    serializer_class = Category1Serializer
    # 第一级分类没有父类
    queryset = GoodsCategory.objects.filter(parent__isnull=True)


# 获取二级和三级分类
class CategoryView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return GoodsCategory.objects.filter(parent_id=self.kwargs.get('pk'))
        # queryset = GoodsCategory.objects
        # pk = self.kwargs.get('pk')
        # if pk:
        #     # 第二级分类
        #     queryset = queryset.filter(parent_id=pk)
        # return queryset
