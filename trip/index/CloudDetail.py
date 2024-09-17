from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from trip.models import CropInfo
from trip.serializers import SceneSpotSerializer
from trip.utils import APIResponse
from trip.utils import MyPage


# 获取一个作物下的所有景点信息
@swagger_auto_schema(method='post', tags=['云种植>作物所在的景点'], operation_summary='这里传入作物信息(cropinfo)的id',
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'name': openapi.Schema(
                                 type=openapi.TYPE_STRING,
                                 description='作物名称'
                             )
                         },
                         required=['name'],
                         example={
                             'name': '苹果'
                         }
                     ),
                     operation_description='返回作物的所有景点信息')
@api_view(['POST'])
def cloud_detail(request):
    name = request.data.get('name')
    crop_infos = CropInfo.objects.filter(name=name)

    try:
        # data = []
        # for crop_info in crop_infos:
        #     serializer = SceneSpotSerializer(crop_info.scene_spot.all(), many=True)
        #     data.extend(serializer.data)
        data = []
        paginator = MyPage()
        for crop_info in crop_infos:
            page = paginator.paginate_queryset(crop_info.scene_spot.all(), request)
            serializer = SceneSpotSerializer(page, many=True)
            data.extend(serializer.data)
    except:
        return APIResponse(code=400, data=None, msg='该名字没有对应的景点信息')
    return paginator.get_paginated_response(data)
