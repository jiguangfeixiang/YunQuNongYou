from trip.models import Product
from trip.serializers import ProductSerializer
from trip.utils import CustomModelViewSet
from trip.utils import MyPage


# 产品的增删改查
class ProductView(CustomModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
