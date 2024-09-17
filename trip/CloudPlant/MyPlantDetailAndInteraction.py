from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers
from rest_framework.decorators import api_view

from trip.models import OwnedCrop
from trip.serializers import OwnedCropSerializer, CropInfoSerializer, GrowRecordSerializer, OwnedCropImageSerializer
from trip.utils import APIResponse


class ImagSerializer(serializers.Serializer):
    image = serializers.ImageField()


@swagger_auto_schema(methods=['GET'], tags=['云种植>种植详情和互动'], operation_summary='在这里传入的是拥有作物的id哦',
                     operation_description='返回作物的详情和互动')
# 传入作物的id
@api_view(['GET', ])
def plant_detail(request, pk):
    # 1.获取数据
    try:
        if request.query_params.get('date'):
            plant = OwnedCrop.objects.get(id=pk, date=request.query_params['date'])
        else:
            plant = OwnedCrop.objects.get(id=pk)
        images = plant.images
        plant_info = plant.crop_info
    except OwnedCrop.DoesNotExist:
        return APIResponse(code=404, status=status.HTTP_404_NOT_FOUND)
    # 2.返回数据
    record = plant.records.filter(record_date=datetime.now().date()).first()
    record = GrowRecordSerializer(record, many=False).data
    if record:
        now_three_images = [
            record.get('photo_morning'),
            record.get('photo_noon'),
            record.get('photo_evening')
        ]
    else:
        APIResponse(data='今天种植记录里没有三张照片', code=400, msg='请农户或者管理员加点数据')
        # 如果记录不存在，则设置图片 URL 为 None
        now_three_images = [None, None, None]
    data = {
        'carousel_images': OwnedCropImageSerializer(images, many=True).data,
        'my_plant': OwnedCropSerializer(plant, many=False).data,
        'today_record_three_images': now_three_images,
        'plant_info': CropInfoSerializer(plant_info, many=False).data
    }
    return APIResponse(code=200, status=status.HTTP_200_OK, data=data)
