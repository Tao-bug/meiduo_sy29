from rest_framework.generics import ListAPIView
from apps.meiduo_admin.serializers.spu import SpuSimpleSerializer
from apps.goods.models import SPU


class SpuSimpleView(ListAPIView):
    queryset = SPU.objects.all()
    serializer_class = SpuSimpleSerializer
