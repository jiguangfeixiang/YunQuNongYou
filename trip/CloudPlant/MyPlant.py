import django_filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers
from rest_framework.decorators import api_view

from trip.models import User, OwnedCrop
from trip.serializers import OwnedCropSerializer
from trip.utils import APIResponse

# 定义请求参数
name_parameter = openapi.Parameter(
    'name', in_=openapi.IN_QUERY,
    description="搜索作物的名称",
    type=openapi.TYPE_STRING
)
buy_date_parameter = openapi.Parameter(
    'buy_date', in_=openapi.IN_QUERY,
    description="在这里是过滤某一天的作物的购买日期，格式为YYYY-MM-DD",
    type=openapi.TYPE_STRING
)
growth_area_parameter = openapi.Parameter(
    'growth_area', in_=openapi.IN_QUERY,
    description="作物的生长区域",
    type=openapi.TYPE_STRING
)


class OwnedCropFilter(django_filters.FilterSet):
    # 使用正确的字段名称
    name = django_filters.CharFilter(field_name='crop_info__name', lookup_expr='contains')
    buy_date = django_filters.DateFilter(field_name='buy_date', lookup_expr='contains')  # 注意这里是 'exact' 不是 'exacts'
    growth_area = django_filters.CharFilter(field_name='crop_info__growth_area', lookup_expr='contains')

    class Meta:
        model = OwnedCrop
        fields = ['name', 'buy_date', 'growth_area']


# 传入用户id
@swagger_auto_schema(methods=['GET'], tags=['云种植>我的种植'],
                     operation_summary='这里要传入用户的id,',
                     operation_description='返回与我的种植相关的图片。',
                     manual_parameters=[name_parameter, buy_date_parameter, growth_area_parameter]

                     )
@api_view(['GET', ])
def my_plant(request, pk):
    try:
        user = User.objects.get(pk=pk)
        owned_crop = user.owned_crops.all()
    except User.DoesNotExist:
        return APIResponse(code='400', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # 根据过滤器进行过滤用户拥有的作物
        filterset = OwnedCropFilter(request.GET, queryset=owned_crop)
        if filterset.is_valid():
            filtered_owned_crop = filterset.qs  # 这里获取过滤后的查询集
            # 默认是购买时间倒序排列
            filtered_owned_crop = filtered_owned_crop.order_by('-buy_date')

        else:
            return APIResponse(code='400', status=status.HTTP_400_BAD_REQUEST, data=filterset.errors)

        # serializer = imageSerializer(filtered_owned_crop, many=True)
        serializer = OwnedCropSerializer(filtered_owned_crop, many=True)
        data = {
            'name': user.username,
            'owned_crop_data': serializer.data,
        }
        return APIResponse(code='200', status=status.HTTP_200_OK, data=data)
