from rest_framework import serializers
from apps.goods.models import SPU


class SpuSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPU
        fields = ['id', 'name']


# 查询获取SPU表列表数据
class SpuSerializer(serializers.ModelSerializer):
    brand_id = serializers.IntegerField()
    category1_id = serializers.IntegerField()
    category2_id = serializers.IntegerField()
    category3_id = serializers.IntegerField()

    class Meta:
        model = SPU
        # fields = '__all__'
        exclude = ['brand', 'category1', 'category2', 'category3']


# 简单品牌信息
class BrandsSimpleSerialiazer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
