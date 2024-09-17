# 景点的增删改查
import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status
from rest_framework.decorators import action

from trip.models import SceneSpot, SceneComment, SceneImage
from trip.serializers import SceneSpotSerializer, CommentSerializer, SceneImageSerializer, \
    SceneActivitySerializer, ScenePlantProjectSerializer, SceneFoodSerializer, ScenePlacePlaySerializer
from trip.utils import CustomModelViewSet, APIResponse, MyPage


class SceneSpotView(CustomModelViewSet):
    queryset = SceneSpot.objects.all()
    serializer_class = SceneSpotSerializer
    pagination_class = MyPage
    # 设计搜索,排序字段
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'belong_province__name', 'city']

    @swagger_auto_schema(
        method='get',
        tags=['景点>详情'],
        operation_summary='返回与景点有关的景点照片,景点评论,景点项目',
        operation_description='返回与景点有关的景点照片,景点评论,景点项目。',
    )
    @action(detail=True, methods=['get'])
    def details(self, request, *args, **kwargs):
        '''
        返回与景点有关的景点照片,景点评论,景点项目
        '''
        try:
            scene_spot = self.get_object()
            scene_spot.visit_count += 1
            scene_plant_project = scene_spot.plant
            scene_activity = scene_spot.scene_activities.all()
            food = scene_spot.scene_foods.all()
        except Exception as e:
            return APIResponse(data={'error': str(e)}, code=400, msg='获取失败', status=status.HTTP_400_BAD_REQUEST)

        comment = SceneComment.objects.filter(scene_spot=scene_spot).order_by('-comment_time')
        scene_place_play = scene_spot.place_play
        # project = scene_spot.projects
        image = SceneImage.objects.filter(scene_spot=scene_spot)
        comment_serializer = CommentSerializer(comment, many=True, context={'request': request})
        # project_serializer = ProjectSerializer(project, many=True, context={'request': request})
        scene_place_play_serializer = ScenePlacePlaySerializer(scene_place_play)
        image_serializer = SceneImageSerializer(image, many=True, context={'request': request})
        scene_plant_project_serializer = ScenePlantProjectSerializer(scene_plant_project,)
        scene_activity = SceneActivitySerializer(scene_activity, many=True, context={'request': request})
        food_serializer = SceneFoodSerializer(food, many=True, context={'request': request})
        data = {
            'plant': scene_plant_project_serializer.data,
            # 'project': project_serializer.data,
            'place_play': scene_place_play_serializer.data,
            'image': image_serializer.data,
            'activity': scene_activity.data,
            'food': food_serializer.data,
            'comment': comment_serializer.data,
        }
        scene_spot.save()
        return APIResponse(data=data, code=200, msg='获取成功', status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['景点>过滤'],
        manual_parameters=[
            # 已存在的自定义参数
            openapi.Parameter('project_start_place', openapi.IN_QUERY, description="项目起点",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('project_destination', openapi.IN_QUERY, description="项目终点",
                              type=openapi.TYPE_STRING),
            # 添加搜索参数
            openapi.Parameter('search', openapi.IN_QUERY, description="搜索字段，可以通过景点名称或所属省份搜索景点",
                              type=openapi.TYPE_STRING),
            # 添加排序参数
            openapi.Parameter('ordering', openapi.IN_QUERY, description="排序字段，可以通过访问计数排序景点",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('project_start_time', openapi.IN_QUERY, description="项目出发时间",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('project_trip_day', openapi.IN_QUERY, description="项目出行天数",
                              type=openapi.TYPE_STRING),
        ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # 重写查询参数
    def get_queryset(self):
        queryset = SceneSpot.objects.all()
        start_place = self.request.query_params.get('project_start_place', None)
        destination = self.request.query_params.get('project_destination', None)
        start_time = self.request.query_params.get('project_start_time', None)
        trip_day = self.request.query_params.get('project_trip_day', None)
        if start_place and destination:
            queryset = queryset.filter(projects__start_place=start_place, projects__destination=destination)
        elif start_place:
            queryset = queryset.filter(projects__start_place=start_place)
        elif destination:
            queryset = queryset.filter(projects__destination=destination)
        elif start_time:
            start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
            queryset = queryset.filter(projects__start_time__date=start_time)

        elif trip_day:
            queryset = queryset.filter(projects__trip_day=trip_day)

        return queryset.order_by('-visit_count').distinct()
