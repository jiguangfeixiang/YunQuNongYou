from django.http import HttpResponse
from rest_framework.decorators import api_view

from trip.serializers import testImageSerializer
from trip.utils import APIResponse


# 定义首页view
def index(request):
    return HttpResponse("宝贝欢迎来到首页呢~")


@api_view(['GET', 'POST'])
def testImage(request):
    if request.method == 'GET':
        return HttpResponse('这是get接口你应该用post接口')
    elif request.method == 'POST':
        image = request.data.get('image')
        serializer = testImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(data=serializer.data, status=200)
        else:
            return HttpResponse("数据无效,不知道是谁的问题")


# # coding: utf-8
#
# from huaweicloudsdkcore.auth.credentials import BasicCredentials
# from huaweicloudsdkcore.auth.credentials import DerivedCredentials
# from huaweicloudsdkiotda.v5.region.iotda_region import IoTDARegion
# from huaweicloudsdkcore.exceptions import exceptions
# from huaweicloudsdkiotda.v5 import *
#
# if __name__ == "__main__":
#     # The AK and SK used for authentication are hard-coded or stored in plaintext, which has great security risks. It is recommended that the AK and SK be stored in ciphertext in configuration files or environment variables and decrypted during use to ensure security.
#     # In this example, AK and SK are stored in environment variables for authentication. Before running this example, set environment variables CLOUD_SDK_AK and CLOUD_SDK_SK in the local environment
#     ak = __import__('os').getenv("CLOUD_SDK_AK")
#     sk = __import__('os').getenv("CLOUD_SDK_SK")
#
#     credentials = BasicCredentials(ak, sk) \
#             .with_derived_predicate(DerivedCredentials.get_default_derived_predicate()) \
#
#     client = IoTDAClient.new_builder() \
#         .with_credentials(credentials) \
#         .with_region(IoTDARegion.value_of("<YOUR REGION>")) \
#         .build()
#
#     try:
#         request = ShowDeviceShadowRequest()
#         response = client.show_device_shadow(request)
#         print(response)
#     except exceptions.ClientRequestException as e:
#         print(e.status_code)
#         print(e.request_id)
#         print(e.error_code)
#         print(e.error_msg)
def test(request):
    pass
