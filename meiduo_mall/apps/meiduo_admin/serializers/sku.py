from rest_framework import serializers
from apps.goods.models import SKU


class SkuSpecRelatedSerializer(serializers.Serializer):
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()


class SkuSerializer(serializers.ModelSerializer):
    # 将标准商品以字符串输出
    spu = serializers.StringRelatedField(read_only=True)
    # 指定all时，隐藏属性需要明确定义
    spu_id = serializers.IntegerField()
    # 指定第三级分类外键输出名称
    category = serializers.StringRelatedField(read_only=True)
    # 指定隐藏属性
    category_id = serializers.IntegerField()
    # 规格信息
    specs = SkuSpecRelatedSerializer(many=True, read_only=True)

    class Meta:
        model = SKU
        # fields = '__all__'
        exclude = ['create_time', 'update_time']

