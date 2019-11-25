from rest_framework import serializers
from apps.goods.models import SPUSpecification


# 商品规格管理
class SpecSerializer(serializers.ModelSerializer):
    # 关联嵌套返回spu表的商品名
    spu = serializers.StringRelatedField(read_only=True)
    # 返回关联spu的id值
    spu_id = serializers.IntegerField()

    class Meta:
        model = SPUSpecification
        fields = ['id', 'name', 'spu', 'spu_id']
        read_only_fields = ['id']
