from rest_framework import serializers
from apps.goods.models import SPU


class SpuSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPU
        fields = ['id', 'name']


# 查询获取SPU表列表数据
class SpuSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField(read_only=True)
    brand_id = serializers.IntegerField(read_only=True)
    category1_id = serializers.IntegerField(read_only=True)
    category2_id = serializers.IntegerField(read_only=True)
    category3_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = SPU
        # fields = '__all__'
        exclude = ['category1', 'category2', 'category3']


# 简单品牌信息
class BrandsSimpleSerialiazer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

