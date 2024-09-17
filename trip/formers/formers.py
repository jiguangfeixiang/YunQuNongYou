from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from trip.models import Former, CropInfo, OwnedCrop, GrowRecord
from trip.serializers import FormerSerializer, CropInfoSerializer, GrowRecordSerializer
from trip.utils import APIResponse

upload_record_three_pic_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['buy_crop_id', 'date', 'morning_pic', 'noon_pic', 'evening_pic'],
    properties={
        'buy_crop_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'date': openapi.Schema(type=openapi.TYPE_STRING),
        'morning_pic': openapi.Schema(type=openapi.TYPE_STRING),
        'noon_pic': openapi.Schema(type=openapi.TYPE_STRING),
        'evening_pic': openapi.Schema(type=openapi.TYPE_STRING),
    },
    example={
        'buy_crop_id': 2,
        'date': '2024-04-13',
        'morning_pic': 'http://127.0.0.1:8000/media/morning.jpg',
        'noon_pic': 'http://127.0.0.1:8000/media/noon.jpg',
        'evening_pic': 'http://127.0.0.1:8000/media/evening.jpg',

    }
)


class FormerViewSet(ModelViewSet):
    queryset = Former.objects.all()
    serializer_class = CropInfoSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        # 获取用户信息
        queryset = Former.objects.filter(pk=pk)
        serializer = FormerSerializer(queryset, many=True)
        return APIResponse(data=serializer.data)

    @swagger_auto_schema(
        method='post',
        tags=['农民'],
        operation_summary='添加作物信息',
        operation_description='为指定农民添加作物信息。',
        request_body=CropInfoSerializer,
        responses={201: CropInfoSerializer()},
    )
    @action(methods=['post'], detail=True)
    def add_crop(self, request, *args, **kwargs):
        queryset = Former.objects.filter(pk=kwargs.get('pk'))
        former = self.get_object()
        serializer = CropInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(former=former)
            return APIResponse(data=serializer.data, status=status.HTTP_201_CREATED)
        return APIResponse(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='delete',
        tags=['农民'],
        operation_summary='传入删除作物的id',
        operation_description='为指定农民删除作物信息。',
    )
    @action(methods=['delete'], detail=True)
    def delete_crop(self, request, *args, **kwargs):
        owned_crop = get_object_or_404(CropInfo, pk=kwargs['pk'])
        owned_crop.delete()
        return APIResponse(code=200, msg='删除成功', data=owned_crop.name, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='get',
        tags=['农民'],
        operation_summary='作物信息浏览,这里传入农民id',
        operation_description='返回所有作物信息',
    )
    @action(methods=['get'], detail=True)
    def crop_info(self, request, *args, **kwargs):
        former = self.get_object()
        crop_info = CropInfo.objects.filter(former=former)
        serializer = CropInfoSerializer(crop_info, many=True)
        return APIResponse(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def show_record(self, request, *args, **kwargs):
        former = self.get_object()
        crop_info = OwnedCrop.objects.filter(crop_info__former__id=former)
        serializer = CropInfoSerializer(crop_info, many=True)
        return APIResponse(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='post',
        tags=['农民'],
        operation_summary='这里上传拥有作物的id,日期,照片',
        operation_description='给拥有的作物添加选定日期的记录三张照片。',
        request_body=upload_record_three_pic_request,
        responses={200: '上传成功'},
    )
    # 给拥有的作物添加选定日期的记录三张照片,也可以修改记录   农民应该给买他的作物也就是拥有作物的选定日期上传三张照片
    @action(methods=['POST'], detail=True)
    def upload_record_three_pic(self, request, *args, **kwargs):
        try:
            buy_crop_id = request.data.get('buy_crop_id')
            date = request.data.get('date')
            morning_pic = request.data.get('morning_pic')
            noon_pic = request.data.get('noon_pic')
            evening_pic = request.data.get('evening_pic')
            # # 获得谁买农民的拥有作物的对象
            # buy_former_crop = OwnedCrop.objects.get(id=buy_crop_id)
            # 获取指定日期的记录
            record = GrowRecord.objects.get(owned_crop_id=buy_crop_id, record_date=date)
            # 根据提供的数据更新记录
            if morning_pic:
                record.photo_morning = morning_pic
            if noon_pic:
                record.photo_noon = noon_pic
            if evening_pic:
                record.photo_evening = evening_pic
            record.save()
            serializer = GrowRecordSerializer(record, many=False)
            return APIResponse(code=200, msg='上传成功', data=serializer.data, status=status.HTTP_200_OK)
        except OwnedCrop.DoesNotExist:
            return APIResponse(code=400, msg='上传失败,拥有作物不存在的', data=None, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return APIResponse(code=400, msg='上传失败', data=f'上传失败: {str(e)}', status=status.HTTP_400_BAD_REQUEST)

    # 获取拥有作物的所有记录
    @swagger_auto_schema(
        method='get',
        tags=['农民'],
        operation_summary='这里传入拥有作物的id,返回所有拥有该作物的记录',
        operation_description='返回所有拥有该作物的记录',
    )
    @action(methods=['get'], detail=True)
    def show_owned_crop_record(self, request, *args, **kwargs):
        owned_crop = get_object_or_404(OwnedCrop, pk=kwargs['pk'])
        records = GrowRecord.objects.filter(owned_crop_id=owned_crop)
        serializer = GrowRecordSerializer(records, many=True)
        return APIResponse(code=200, data=serializer.data, status=status.HTTP_200_OK)
