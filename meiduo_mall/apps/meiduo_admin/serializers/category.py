from rest_framework import serializers


# sku-第三级分类
class Category3Serializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
