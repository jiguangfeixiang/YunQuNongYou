from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from trip.models import Message, User, Former
from trip.serializers import MessageSerializer
from trip.utils import APIResponse

'''
这里做四个功能
1.用户发给农户信息
2.农户发给用户信息
3.用户看到所有发的信息
4.农户看到所有发的信息
'''

user_to_former_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['content', 'sender_user_id', 'receiver_former_id', ],
    properties={
        'content': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='内容'
        )
        , 'sender_user_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='发送者用户id', )
        , 'receiver_former_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='接收者农户id', )
    },
    example={
        'content': '你好',
        'sender_user_id': 1,
        'receiver_former_id': 1
    }
)

former_to_user_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['content', 'sender_former_id', 'receiver_user_id', ],
    properties={
        'content': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='内容'
        )
        , 'sender_former_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='发送者农民id', )
        , 'receiver_user_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='接收者用户id', )
    },
    example={
        'content': '你好',
        'sender_former_id': 1,
        'receiver_user_id': 1
    }
)


@swagger_auto_schema(methods=['POST'], tags=['云种植>用户与农户交流'], operation_summary='这里是用户发送给农户信息',
                     request_body=user_to_former_request_body,
                     responses={200: '发送成功', 400: '发送失败', 500: '发送失败'}
                     )
@api_view(['POST'])
def user_to_former(request, ):
    content = request.data.get('content')
    send_user = request.data.get('sender_user_id')
    send_user = User.objects.get(id=send_user)
    receiver_former = request.data.get('receiver_former_id')
    receiver_former = Former.objects.get(id=receiver_former)
    data = Message.objects.create(content=content, sender_user=send_user, receiver_former=receiver_former)
    serializer = MessageSerializer(data)
    return APIResponse(code=200, message='发送成功', data=serializer.data)


@swagger_auto_schema(methods=['POST'], tags=['云种植>用户与农户交流'], operation_summary='这里是农户发送给用户信息',
                     request_body=former_to_user_request_body,  # 可以复用或根据需要调整
                     responses={200: '发送成功', 400: '发送失败', 500: '发送失败'}
                     )
@api_view(['POST'])
def former_to_user(request):
    content = request.data.get('content')
    send_former = request.data.get('sender_former_id')
    send_former = Former.objects.get(id=send_former)
    receiver_user = request.data.get('receiver_user_id')
    receiver_user = User.objects.get(id=receiver_user)
    data = Message.objects.create(content=content, sender_former=send_former, receiver_user=receiver_user)
    serializer = MessageSerializer(data)
    return APIResponse(code=200, message='发送成功', data=serializer.data)


@swagger_auto_schema(methods=['GET'], tags=['云种植>用户与农户交流'], operation_summary='这里是用户所有的聊天',
                     responses={200: '发送成功', 400: '发送失败', 500: '发送失败'}
                     )
@api_view(['GET'])
def user_messages(request, user_id):
    user = User.objects.get(id=user_id)
    user_send_message = user.send_message.all().order_by('-time')
    send_serializer = MessageSerializer(user_send_message, many=True)
    user_receive_message = Message.objects.filter(receiver_user=user).order_by('-time')
    receive_serializer = MessageSerializer(user_receive_message, many=True)
    data = {
        'user_send_message': send_serializer.data,
        'user_receive_message': receive_serializer.data,
    }
    return APIResponse(code=200, message='收到成功', data=data)


@swagger_auto_schema(methods=['GET'], tags=['云种植>用户与农户交流'], operation_summary='这里是农户所有的聊天',
                     responses={200: '发送成功', 400: '发送失败', 500: '发送失败'}
                     )
@api_view(['GET'])
def former_messages(request, former_id):
    former = Former.objects.get(id=former_id)
    former_send_message = former.send_message.all().order_by('-time')
    send_serializer = MessageSerializer(former_send_message, many=True)
    former_receive_message = Message.objects.filter(receiver_former=former).order_by('-time')
    receive_serializer = MessageSerializer(former_receive_message, many=True)
    data = {
        'former_send_message': send_serializer.data,
        'former_receive_message': receive_serializer.data,
    }
    return APIResponse(code=200, message='收到成功', data=data)
