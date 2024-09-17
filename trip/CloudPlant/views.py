from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

from trip.models import CropCareTask, UserOperationHistory, User, OwnedCrop, CropInfo
from trip.serializers import UserOperationHistorySerializer, CropInfoSerializer
from trip.utils import APIResponse, MyPage

task_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['task_type', 'owned_crop_id', ],
    properties={
        'task_type': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='正在执行的任务类型water, fertilize, weed,pest'),
        'owned_crop_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='执行任务的拥有作物的ID')
    },
    example={
        'task_type': 'fertilize',
        'owned_crop_id': 1,
    }
)


@swagger_auto_schema(
    method='POST',
    tags=['云种植>养护任务'],
    operation_summary='传入用户拥有作物的id',
    operation_description='返回的浇水,施肥,除草的数量和当前记录(types是none的操作历史',
    request_body=task_request_body,

    responses={200: '任务成功处理', 400: '任务类型无效'}
)
# 养护任务管理
@api_view(['POST', ])
def task_handler(request):
    owned_crop_id = request.data.get('owned_crop_id')
    owned_crop = get_object_or_404(OwnedCrop, id=owned_crop_id)

    record_date = datetime.now().strftime('%Y-%m-%d')
    record, created = owned_crop.records.get_or_create(record_date=record_date)
    # 获取到记录下的任务id
    task_id = record.care_task.id
    current_task_care = get_object_or_404(CropCareTask, id=task_id)
    user_id = OwnedCrop.objects.filter(id=owned_crop_id).first().owner.id
    user = get_object_or_404(User, id=user_id)
    task_type = request.data.get('task_type')

    content = UserOperationHistory.objects.filter(user=user)
    content = content.order_by('-action_date')
    serializer_operation = UserOperationHistorySerializer(content, many=True)

    if task_type == 'water':
        history = UserOperationHistory.objects.create(user=user, action_date=datetime.now(), action_type='浇水任务',
                                                      description=f'{user.username}在{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}给{owned_crop.crop_info.name}完成了浇水任务')
        current_task_care.water_count += 1
        current_task_care.save()
        data = {
            'water_count': current_task_care.water_count,
            'fertilize_count': current_task_care.fertilize_count,
            'weed_count': current_task_care.weed_count,
            'pest_status': current_task_care.task_pest,
            'history': serializer_operation.data
        }
        return APIResponse(code=200, msg='浇水任务成功', data=data)
    elif task_type == 'fertilize':
        current_task_care.fertilize_count += 1
        current_task_care.save()
        history = UserOperationHistory.objects.create(user=user, action_date=datetime.now(), action_type='施肥任务',
                                                      description=f'{user.username}在{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}给{owned_crop.crop_info.name}完成了浇肥任务')

        data = {
            'water_count': current_task_care.water_count,
            'fertilize_count': current_task_care.fertilize_count,
            'pest_status': current_task_care.task_pest,
            'weed_count': current_task_care.weed_count,
            'history': serializer_operation.data
        }
        return APIResponse(code=200, msg='施肥任务成功', data=data)
    elif task_type == 'weed':
        current_task_care.weed_count += 1
        current_task_care.save()
        history = UserOperationHistory.objects.create(user=user, action_date=datetime.now(), action_type='除草',
                                                      description=f'{user.username}在{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}给{owned_crop.crop_info.name}完成了除草任务')
        data = {
            'water_count': current_task_care.water_count,
            'fertilize_count': current_task_care.fertilize_count,
            'weed_count': current_task_care.weed_count,
            'pest_status': current_task_care.task_pest,
            'history': serializer_operation.data
        }
        return APIResponse(code=200, msg='除草任务成功', data=data)
    elif task_type == 'pest':
        current_task_care.task_pest = True
        history = UserOperationHistory.objects.create(user=user, action_date=datetime.now(), action_type='虫害',
                                                      description=f'{user.username}在{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}给{owned_crop.crop_info.name}完成了虫害任务')
        data = {
            'water_count': current_task_care.water_count,
            'fertilize_count': current_task_care.fertilize_count,
            'weed_count': current_task_care.weed_count,
            'pest_status': current_task_care.task_pest,
            'history': serializer_operation.data
        }
        return APIResponse(code=200, msg='除害任务成功', data=data)
    elif task_type == 'none':
        data = {
            'water_count': current_task_care.water_count,
            'fertilize_count': current_task_care.fertilize_count,
            'weed_count': current_task_care.weed_count,
            'pest_status': current_task_care.task_pest,
            'history': serializer_operation.data
        }
        return APIResponse(code=400, msg='获取当前用户所有的操作历史', data=data)


# 返回所有的作物信息
@swagger_auto_schema(method='get', tags=['云种种植>所有作物信息'],
                     operation_summary='传入用户id则返回所有不含当前用户拥有的作物信息,id=0返回所有作物', )
@api_view(['GET', ])
def crop_list(request, user_id):
    if user_id:
        owned_crops = OwnedCrop.objects.filter(owner_id=user_id)

        crops_exclude_id = [owned_crop.crop_info.id for owned_crop in owned_crops]
        crops = CropInfo.objects.exclude(id__in=crops_exclude_id, state='purchased')
    elif user_id == 0:
        crops = CropInfo.objects.all()
    else:
        crops = CropInfo.objects.all(state='purchase')
    crops = crops.filter(state='purchase').order_by('-id')
    pagination = MyPage()
    data = pagination.paginate_queryset(crops, request)
    serializer = CropInfoSerializer(data, many=True)
    return pagination.get_paginated_response(data=serializer.data)


# 处理作物的购买接口
@swagger_auto_schema(methods=['POST', ], tags=['云种种>购买和取消作物'],
                     operation_summary='这里是购买和取消购买的接口,传入三个信息',
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         required=['crop_buy_id', 'user_id', 'if_buy'],
                         properties={
                             'crop_buy_id': openapi.Schema(type=openapi.TYPE_STRING, description='购买的作物'),
                             'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='用户id'),
                             'if_buy': openapi.Schema(type=openapi.TYPE_STRING, description='是否购买,默认为Ture'),
                         },
                         example={
                             'crop_buy_id': '1',
                             'user_id': '1',
                             'if_buy': 'true',
                         }
                     ),
                     responses={200: '购买成功'}
                     )
@api_view(['POST'])
def crop_buy(request):
    crop_buy_id = request.data.get('crop_buy_id')
    user_id = request.data.get('user_id')
    if_buy = request.data.get('if_buy')

    user = get_object_or_404(User, id=user_id)
    cropinfo = get_object_or_404(CropInfo, id=crop_buy_id)

    if cropinfo.state == 'purchased' and if_buy == 'true':
        return APIResponse(code=400, msg='该作物已经购买过了')
    elif cropinfo.state == 'purchase' and if_buy == 'true':
        if OwnedCrop.objects.filter(owner=user, crop_info=cropinfo).exists():
            return APIResponse(code=400, msg=f'{OwnedCrop.owner.username}用户已经购买过该作物')
        cropinfo.state = 'purchased'
        cropinfo.save()
        # 检查是否已经存在具有相同 crop_info 的 OwnedCrop 对象
        owned_crop, created = OwnedCrop.objects.get_or_create(owner=user, crop_info=cropinfo)
        if created:
            owned_crop.save()
            # 如果新创建了对象，返回成功购买的响应
            return APIResponse(code=200, msg='购买成功', data={'owned_crop_id': owned_crop.id})
        else:
            # 如果对象已存在，返回购买过的响应
            return APIResponse(code=200, msg='已购买过该作物', data={'owned_crop_id': owned_crop.id})

    elif cropinfo.state == 'purchased' and if_buy == 'false':
        cropinfo.state = 'purchase'
        owned_crop = OwnedCrop.objects.filter(owner=user, crop_info=cropinfo).first()
        if owned_crop:
            owned_crop.delete()  # 删除已存在的 OwnedCrop 对象
        cropinfo.save()
        return APIResponse(code=200, msg='取消成功')
    elif cropinfo.state == 'purchase' and if_buy == 'false':
        return APIResponse(code=400, msg='该作物还没有购买过，无法取消购买')
    else:
        return APIResponse(code=400, msg='参数错误')
