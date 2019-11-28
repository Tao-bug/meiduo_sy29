from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from fdfs_client.client import Fdfs_client
from apps.goods.models import SKUImage
from apps.meiduo_admin.serializers.images import ImageSerializer
from apps.meiduo_admin.utils.meiduo_pagination import MeiduoPagination
from django.conf import settings


# sku图片
class ImageViewSet(ModelViewSet):
    queryset = SKUImage.objects.order_by('-id')
    serializer_class = ImageSerializer
    pagination_class = MeiduoPagination

    # 重写创建方法，原因：默认代码只有创建对象的功能，不包含上传图片的功能
    def create(self, request, *args, **kwargs):
        # 接受
        sku_id = request.data.get('sku')  # sku编号
        image_file = request.data.get('image')  # 图片文件对象

        # 验证
        if not all([sku_id, image_file]):
            return serializers.ValidationError('数据不完全')

        # 处理
        # 上传图片
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        result = client.upload_by_buffer(image_file.read())
        image_name = result.get('Remote file_id')
        # 创建对象
        instance = SKUImage.objects.create(sku_id=sku_id, image=image_name)
        # 响应
        return Response({
            'id': instance.id,
            'sku': instance.sku_id,
            'image': instance.image.url
        })

    # 重写修改方法，原因：默认代码中只侯对象，不包含图片修改
    def update(self, request, *args, **kwargs):
        instance = SKUImage.objects.get(pk=self.kwargs.get('pk'))
        # 接受
        sku_id = request.data.get('sku')
        image_file = request.data.get('image')

        # 校验
        if not all([sku_id, image_file]):
            raise serializers.ValidationError('数据不完整')

        # 处理图片
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        # 删除原有图片
        client.delete_file(instance.image.name)
        # 添加新图片
        result = client.upload_by_buffer(image_file.read())
        image_name = result.get('Remote file_id')

        # 修改模型类对象
        instance.sku_id = sku_id
        instance.image = image_name
        instance.save()

        # 响应
        return Response({
            'id': instance.id,
            'sku': instance.sku_id,
            'image': instance.image.url
        })

    def destroy(self, request, *args, **kwargs):
        instance = SKUImage.objects.get(pk=self.kwargs.get('pk'))

        # 删除fastdfs中的图片
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        client.delete_file(instance.image.name)

        instance.delete()
        return Response(status=204)