from drf_yasg.utils import swagger_auto_schema

from trip.models import Province
from trip.serializers import ProvinceSerializer
from trip.utils import CustomModelViewSet


# 省的查
class ProvinceView(CustomModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

