from rest_framework.serializers import ModelSerializer
from apps.goods.models import Brand


class BrandSerializer(ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'
