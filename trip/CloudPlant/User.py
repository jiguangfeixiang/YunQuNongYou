from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view

from trip.models import User, OwnedCrop
from trip.serializers import UserSerializer
from trip.utils import APIResponse


@swagger_auto_schema(methods=['GET'], tags=['云种植>种植首页'])
@swagger_auto_schema(methods=['POST'], tags=['云种植>种植首页'])
@api_view(['GET', 'POST'])
def user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        crop = OwnedCrop.objects.filter(owner=user)
        crop_num = crop.count()
    except User.DoesNotExist:
        return APIResponse(code='400', status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        data = {
            'user': serializer.data,
            'crop_num': crop_num,
        }

        # 把crop_num加到data里

        return APIResponse(data=data)
