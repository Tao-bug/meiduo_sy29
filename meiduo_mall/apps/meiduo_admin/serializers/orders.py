from rest_framework import serializers
from apps.orders.models import OrderInfo


# 订单
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ['order_id', 'create_time']


class SkuSerializer(serializers.Serializer):
    name = serializers.CharField
    default_image = serializers.ImageField()


class OrderGoodsSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    sku = SkuSerializer(read_only=True)


# 详细订单
class OrderDetailSerializer(serializers.ModelSerializer):
    # 输出显示用户名
    user = serializers.StringRelatedField(read_only=True)

    # 输出显示订单商品
    skus = OrderGoodsSerializer(many=True, read_only=True)
    class Meta:
        model = OrderInfo
        fields = '__all__'
