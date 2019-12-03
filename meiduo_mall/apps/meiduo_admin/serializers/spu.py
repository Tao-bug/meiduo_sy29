from rest_framework import serializers
from apps.goods.models import SPU


class SpuSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPU
        fields = ['id', 'name']


# 查询获取SPU表列表数据
class SpuSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    brand_id = serializers.IntegerField()
    category1_id = serializers.IntegerField()
    category2_id = serializers.IntegerField()
    category3_id = serializers.IntegerField()
    # category1 = serializers.CharField(read_only=True)
    # category2 = serializers.CharField(read_only=True)
    # category3 = serializers.CharField(read_only=True)

    class Meta:
        model = SPU
        # fields = '__all__'
        exclude = ['category1', 'category2', 'category3']


# 简单品牌信息
class BrandsSimpleSerialiazer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
