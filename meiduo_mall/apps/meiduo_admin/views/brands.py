from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from fdfs_client.client import Fdfs_client
from django.conf import settings
from apps.goods.models import Brand
from apps.meiduo_admin.serializers.brands import BrandSerializer
from apps.meiduo_admin.utils.meiduo_pagination import MeiduoPagination


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.order_by('-id')
    serializer_class = BrandSerializer
    pagination_class = MeiduoPagination

    # 重写创建方法，原因：默认代码只有创建对象的功能，不包含上传图片的功能
    def create(self, request, *args, **kwargs):
        # 接受参数
        name = request.data.get('name')
        first_letter = request.data.get('first_letter')
        logo_file = request.data.get('logo')

        # 校验
        if not all([name, first_letter, logo_file]):
            return serializers.ValidationError('数据不完全')

        # 数据处理
        # 上传图片
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        result = client.upload_by_buffer(logo_file.read())
        logo_name = result.get('Remote file_id')

        # 创建对象
        instance = Brand.objects.create(name=name, first_letter=first_letter, logo=logo_name)

        # 返回响应
        return Response({
            'id': instance.id,
            'name': instance.name,
            'logo': instance.logo,
            'first_letter': instance.first_letter
        })

    #
    def update(self, request, *args, **kwargs):

        return
