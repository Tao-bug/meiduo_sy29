from rest_framework import serializers
from apps.goods.models import SPUSpecification, SpecificationOption


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


class OptionRelatedSerialiazer(serializers.Serializer):
    id = serializers.IntegerField()
    value = serializers.CharField()


# sku-根据spu_id查询规格及选项
class SpecBySpuSerializer(serializers.Serializer):
    # 根据标准商品编号，查询规格及选项
    id = serializers.IntegerField()
    name = serializers.CharField()
    spu = serializers.StringRelatedField(read_only=True)
    spu_id = serializers.IntegerField()
    # 规格与选项为1对多关系，在选项中定义了规格外键，通过参数related_name指定options
    options = OptionRelatedSerialiazer(many=True, read_only=True)


# 规格选项表管理
# 查询获取规格选项表列表数据
class SpecOptionSerializer(serializers.ModelSerializer):
    spec = serializers.StringRelatedField()
    spec_id = serializers.IntegerField()

    class Meta:
        model = SpecificationOption
        fields = '__all__'
        read_only_fields = ['id']


# 下拉菜单获取品牌信息
class SpecSimpleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

