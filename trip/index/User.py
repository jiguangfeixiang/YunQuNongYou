from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

from trip.models import User, Former, SceneComment, SceneSpot
from trip.serializers import UserSerializer, FormerSerializer, CommentSerializer
from trip.utils import APIResponse

register_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['username', 'password', 'repassword', 'phone'],
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
        'repassword': openapi.Schema(type=openapi.TYPE_STRING, description='确认密码'),
        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='手机号码'),
        'avatar': openapi.Schema(type=openapi.TYPE_FILE, description='头像'),
        'types': openapi.Schema(type=openapi.TYPE_STRING, description='用户类型'),
    },
    example={
        'username': 'johndoe',
        'password': 'password123',
        'repassword': 'password123',
        'phone': '1234567890',
        'avatar': None,
        'types': 'User',
    }
)
login_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['username', 'password', 'types', ],
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
        'types': openapi.Schema(type=openapi.TYPE_STRING, description='用户类型'),
    },
    example={
        'username': 'johndoe',
        'password': 'password123',
        'types': 'User',
    }
)


#
# class UserViewSet(CustomModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


@swagger_auto_schema(method='post', tags=['用户农民登录注册'],
                     request_body=register_request_body,
                     responses={200: '登录成功'}
                     )
@api_view(['POST'])
def register(request):
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    repassword = request.data.get('repassword', None)
    phone = request.data.get('phone', None)
    avatar = request.data.get('avatar', None)
    print(username, password, repassword)
    types = request.data.get('types', None)
    if not username or not password or not repassword:
        return APIResponse(code=400, msg='用户名或密码或确定密码不能为空哦')
    if password != repassword:
        return APIResponse(code=400, msg='密码不一致')
    if types == 'User':
        print(username)
        user = User.objects.filter(username=username).first()
        if user:
            return APIResponse(code=400, msg='用户名已存在')
        user = User.objects.create(username=username, password=password, phone=phone, avatar=avatar, )
        user.save()
        return APIResponse(code=200, msg='注册成功', data=UserSerializer(user).data)
    if types == 'Former':
        former = Former.objects.filter(username=username).first()
        if former:
            return APIResponse(code=400, msg='农户已存在')
        former = Former.objects.create(username=username, password=password, phone=phone, avatar=avatar, )
        former.save()
        return APIResponse(code=200, msg='注册成功', data=FormerSerializer(former).data)


@swagger_auto_schema(method='post', tags=['用户农民登录注册'],
                     request_body=login_request_body,
                     responses={200: '登录成功'}
                     )
@api_view(['POST'])
def login(request):
    username = request.data.get('username', None)
    password = request.data.get('password', None)

    types = request.data.get('types', None)
    if not username or not password:
        return APIResponse(code=200, msg='用户名或密码不能为空')
    if types == 'User':
        user = User.objects.filter(username=username).first()
        if not user:
            return APIResponse(code=400, msg='用户名不存在')
        # 检验密码正确性
        if user.password == password:
            return APIResponse(code=200, msg='登录成功', data=UserSerializer(user).data)
        else:
            return APIResponse(code=400, msg='密码错误')
    if types == 'Former':
        former = Former.objects.filter(username=username).first()
        if not former:
            return APIResponse(code=400, msg='农户不存在')
        if former.password == password:
            return APIResponse(code=200, msg='登录成功', data=FormerSerializer(former).data)
        else:
            return APIResponse(code=400, msg='密码错误')


comment_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['types', 'content', 'image', 'business_comment', 'rating', 'user_id', 'scene_spot_id'],
    properties={
        'types': openapi.Schema(type=openapi.TYPE_STRING, description='评论类型'),
        'content': openapi.Schema(type=openapi.TYPE_STRING, description='评论内容'),
        # 'image': openapi.Schema(type=openapi.TYPE_FILE, description='图片'),
        'business_comment': openapi.Schema(type=openapi.TYPE_STRING, description='商家评论'),
        'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='评分'),
        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='用户id'),
        'scene_spot_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='景点id'),
    },
    example={
        'types': 'true',
        'content': '评论内容',
        # 'image': None,
        'business_comment': None,
        'rating': 5,
        'user_id': 1,
        'scene_spot_id': 1,
    }
)

delete_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['comment_id'],
    properties={
        'comment_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='评论删除id')
    },
    example={
        'comment_id': 1,
    }
)


# 用户评论接口
@swagger_auto_schema(method='post', tags=['景点>用户评论接口'],
                     operation_summary='用户评论接口',
                     request_body=comment_request_body,
                     responses={200: '评论成功'}
                     )
@api_view(['POST'])
def comment(request):
    data = request.data
    types = data.get('types', None)
    user_id = data.get('user_id')
    scene_spot_id = data.get('scene_spot_id')
    if types == 'true':
        user = get_object_or_404(User, pk=user_id)
        scene_spot = get_object_or_404(SceneSpot, pk=scene_spot_id)
        # 此处应根据你的业务逻辑提取其他必要字段
        content = data.get('content', '')
        # image = data.get('image', None)
        avatar = user.avatar
        rating = data.get('rating', 0)
        business_comment = data.get('business_comment', None)
        data = SceneComment.objects.create(user=user,
                                           scene_spot=scene_spot,
                                           content=content,
                                           image=avatar,
                                           rating=rating,
                                           business_comment=business_comment)
        serializer = CommentSerializer(data)
        return APIResponse(code=200, msg='评论成功', data=serializer.data)


@swagger_auto_schema(method='post', tags=['用户评论接口'],
                     operation_summary='用户评论删除',
                     request_body=comment_request_body,
                     responses={200: '删除成功'}
                     )
@api_view(['POST'])
def comment_delete(request):
    comment_id = request.data.get('comment_id', None)
    if comment_id:
        comment = get_object_or_404(SceneComment, pk=comment_id)
        comment.delete()
        return APIResponse(code=200, msg='删除成功')
