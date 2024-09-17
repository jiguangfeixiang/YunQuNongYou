from django.urls import path, include
from rest_framework import routers

from trip import views
from trip.CloudPlant import urls as plant_urls
from trip.index.CloudDetail import cloud_detail
from trip.index.Product import ProductView
from trip.index.Province import ProvinceView
from trip.index.Scene import SceneSpotView
from trip.index.User import *
from trip.index.gpt import gptInterface
from .formers.formers import FormerViewSet

# 视图集路由
router = routers.DefaultRouter()
router.register(r'products', ProductView, basename='产品')
router.register(r'province', ProvinceView)
router.register(r'scene_spots', SceneSpotView)
router.register(r'Formers', FormerViewSet, basename='formers')
# 路由
urlpatterns = [
    path('user/register', register, name='register'),
    path('user/login', login, name='login'),
    path('index/', include(router.urls)),
    path('index/gpt', gptInterface, name='gpt'),
    path('index/scnene_spot/comment', comment, name='用户评论'),
    path('index/scnene_spot/commentdelete', comment_delete, name='用户评论'),
    path('plant/', include(plant_urls), name='用户种植'),
    path('index/crop_scene/', cloud_detail, name='作物所属景点'),
    path('', views.index, name='index'),
]
