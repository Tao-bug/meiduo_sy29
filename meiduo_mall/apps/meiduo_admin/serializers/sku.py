from rest_framework import serializers
from django.db import transaction
from apps.goods.models import SKU, SKUSpecification
from celery_tasks.detail.tasks import task_generate


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
    # specs = SkuSpecRelatedSerializer(many=True, read_only=True)
    # 创建sku时，需要接收规格数据，删除read_only=True参数
    specs = SkuSpecRelatedSerializer(many=True)

    class Meta:
        model = SKU
        # fields = '__all__'
        exclude = ['create_time', 'update_time']

    # 重写创建
    def create(self, validated_data):
        # SKU对应的表中没有属性specs，所以需要从字典中删除
        specs = validated_data.pop('specs')

        with transaction.atomic():  # 禁止自动提交
            sid = transaction.savepoint()  # 开启事务
            try:
                # 创建sku对象
                instance = SKU.objects.create(**validated_data)
                # 遍历，创建sku规格对象
                for item in specs:
                    spec_id = item.get('spec_id')  # 规格编号
                    option_id = item.get('option_id')  # 选项编号
                    SKUSpecification.objects.create(sku_id=instance.id, spec_id=spec_id, option_id=option_id)
            except Exception as e:
                transaction.savepoint_rollback(sid)  # 回滚事务
                return serializers.ValidationError('数据保存失败')
            else:
                transaction.savepoint_commit(sid)  # 提交事务

                # 为sku生成静态文件
                task_generate.delay(instance.id)

                return instance

    # 重写修改
    def update(self, instance, validated_data):
        # 事务
        with transaction.atomic():  # 禁止自动提交
            sid = transaction.savepoint()  # 开启事务
            try:
                # validated_data包含了sku所需以外的数据specs,需要先取出
                specs = validated_data.pop('specs')
                # 修改sku
                instance = super().update(instance, validated_data)
                # 修改sku 规格
                # 先删除原有ｓｋｕ规格
                SKUSpecification.objects.filter(sku_id=instance.id).delete()
                for item in specs:
                    # 再新增ｓｋｕ规格
                    item['sku_id'] = instance.id
                    SKUSpecification.objects.create(**item)

            except:
                transaction.savepoint_rollback(sid)
                raise serializers.ValidationError('修改ｓｋｕ失败')
            else:
                transaction.savepoint_commit(sid)

                # 生成静态文件
                task_generate.delay(instance.id)

        return instance


# 图片-查询sku简单数据
class SkuSimpleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()