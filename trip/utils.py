from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import exception_handler


# 自定义分页类
class MyPage(PageNumberPagination):
    page_size = 8
    # 不限制最低页数
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data, ):
        previous_page_url = self.get_previous_link()
        next_page_url = self.get_next_link()
        if self.page.has_next():
            next_page = self.page.next_page_number()
        else:
            next_page = None
        if self.page.has_previous():
            previous_page = self.page.previous_page_number()
        else:
            previous_page = None
        return APIResponse(data=data, code=200, msg='消息成功',
                           count=self.page.paginator.count, next_page=next_page,
                           previous_page=previous_page,
                           next_page_url=next_page_url, previous_page_url=previous_page_url
                           )


# api返回数据处理
class APIResponse(Response):
    def __init__(self, code=200, data=None, msg='消息成功', status=None, count=None, next_page=None, next_page_url=None,
                 previous_page=None, previous_page_url=None,
                 *args, **kwargs):
        if isinstance(data, Serializer):
            msg = (
                '数据格式不正确，请检查数据格式是否正确'
            )
        elif isinstance(data, dict) or isinstance(data, list):
            pass
        else:
            pass
        if count:
            self.data = {'code': code, 'msg': msg, 'data': data, 'count': count, 'next_page': next_page,
                         'next_page_url': next_page_url,
                         'previous_page': previous_page,
                         'previous_page_url': previous_page_url}
        else:
            self.data = {'code': code, 'msg': msg, 'data': data, }
        self.data.update(kwargs)
        super().__init__(data=self.data, status=status)


# 自定义消息返回格式
class CustomModelViewSet(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return APIResponse(data=serializer.data, code=201, msg='创建成功', status=status.HTTP_201_CREATED,
                           headers=headers)

    # 重写ListModelMixin类中的list()方法
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # 应用分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(data=serializer.data)
        # 如果没有分页就不发生分页,或者根据某些条件进行分页
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse(data=serializer.data, code=200, msg='获取成功', status=status.HTTP_200_OK)

    # 重写RetrieveModelMixin类中的retrieve()方法
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return APIResponse(data=serializer.data, code=200, msg='获取成功', status=status.HTTP_200_OK)

    # 重写UpdateModelMixin类中的update()方法
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return APIResponse(data=serializer.data, code=200, msg='更新成功', status=status.HTTP_200_OK)

    # 重写DestroyModelMixin类中的destroy()方法
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return APIResponse(data=None, code=200, msg='删除成功', status=status.HTTP_200_OK)


# 异常处理
def custom_exception(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data.clear()
        response.data['code'] = response.status_code

        if response.status_code == 400:
            response.data['msg'] = '参数错误'
        elif response.status_code == 401:
            response.data['msg'] = '未登录'
        elif response.status_code == 403:
            response.data['msg'] = '无权限'
        elif response.status_code == 404:
            response.data['msg'] = '资源不存在'
        elif response.status_code == 405:
            response.data['msg'] = '请求方法不允许'
        elif response.status_code == 500:
            response.data['msg'] = '服务器内部错误'
        else:
            response.data['msg'] = '未知错误'

        response.data['data'] = {}  # 或者设置为 None，或者基于 `exc` 的信息来填充
        return response
