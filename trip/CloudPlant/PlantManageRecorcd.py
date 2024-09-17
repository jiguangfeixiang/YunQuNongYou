import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view

from trip.models import OwnedCrop
from trip.serializers import GrowRecordImageSerializer, \
    GrowRecordSerializer, CropCareTaskSerializer
from trip.utils import APIResponse


@swagger_auto_schema(methods=['GET'], tags=['云种植>过去十天的记录'], operation_summary='这里传入作物的id')
# 传入作物的id
@api_view(['GET'])
def manage_record(request, pk):
    try:
        owned_crop = OwnedCrop.objects.get(pk=pk)
        now_date = datetime.datetime.now().date()
        ten_days_ago = now_date - datetime.timedelta(days=10)
        # 过滤出当天过去十天日期的生长记录
        now_records = owned_crop.records.filter(record_date__gte=ten_days_ago).order_by('-record_date')
        # 通过当天记录过滤出种植关心任务
        # 通过当天记录过滤出所有图片
    except OwnedCrop.DoesNotExist or True:
        return APIResponse(status=status.HTTP_404_NOT_FOUND, message='作物不存在')
    if request.method == 'GET':
        now_record_care_task_data = []
        now_record_images_data = []
        for now_record in now_records:
            if hasattr(now_record, 'care_task'):
                now_record_care_task_data.append(CropCareTaskSerializer(now_record.care_task).data)
            if hasattr(now_record, 'images'):
                now_record_images_data.append(GrowRecordImageSerializer(now_record.images, many=True).data)
        data = {
            '用户名': owned_crop.owner.username,
            '用户拥有作物的名称': owned_crop.crop_info.name,
            '现在的日期': now_date.strftime('%Y-%m-%d'),
            # 'now_record_care_task': now_record_care_task_data,
            # 'now_record_image': now_record_images_data,
            '过去十天的记录': GrowRecordSerializer(now_records, many=True).data,
        }
        return APIResponse(data=data, status=status.HTTP_200_OK)
