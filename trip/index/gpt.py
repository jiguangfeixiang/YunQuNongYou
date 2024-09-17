from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from openai import OpenAI
from rest_framework.decorators import api_view
from rest_framework.response import Response


def gptInterace(question):
    client = OpenAI(
        base_url="https://api.wlai.vip/v1",
        api_key="sk-gBObv5UI931d72uNA54c0b52Ec6a4d8cBcCf99A1127aD058"
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{question}"}
        ]
    )
    response = completion.choices[0].message.content
    return response


# gpt接口
@swagger_auto_schema(
    method='post',
    tags=['gpt'],
    operation_description="使用 GPT 模型生成回答",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'question': openapi.Schema(type=openapi.TYPE_STRING, description='提问内容'),
        },
        required=['question'],
    ),
    responses={200: openapi.Response('请求成功', openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'code': openapi.Schema(type=openapi.TYPE_INTEGER, description='状态码'),
            'msg': openapi.Schema(type=openapi.TYPE_STRING, description='消息'),
            'data': openapi.Schema(type=openapi.TYPE_STRING, description='GPT模型的回答'),
        }
    )),
               400: openapi.Response('请求失败')}
)
# gpt接口
@api_view(['POST'])
def gptInterface(request):
    question = request.data.get('question')
    if question:
        response = gptInterace(question)
        # 自定义消息格式
        data = {'code': 200, 'msg': '请求成功', 'data': response}
        return Response(data)
    else:
        data = {'code': 400, 'msg': '请求失败', 'data': ''}
        return Response(data)
