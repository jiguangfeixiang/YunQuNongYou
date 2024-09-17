"""
URL configuration for AgricultureTrip project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from trip import urls as trip, views
from trip.views import index

schema_view = get_schema_view(
    openapi.Info(
        title="农业旅游接口文档",
        description="文档描述",
        default_version='v1',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@sample.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# from django.conf import settings
# from django.urls import path, re_path
# from django.views import static
urlpatterns = [
                  path('admin/', admin.site.urls),
                  re_path(r"upload/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}, name='media'),
                  path('trip/', include(trip)),
                  path('', index, name='首页'),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  # path('upload/image/', testImage, name='图片上传'),
                  path('test/', views.test, name='硬件测试'),
re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
                  # 静态文件
                  # re_path(r"^static/(?P<path>.*)", static.serve, {"document root": settings.STATIC_ROOT},
                  #         name="static"),
                  # # 媒体文件
                  # re_path(r"^media/(?P<path>.*)", static.serve, {"document_root": settings.MEDIA_ROOT}, name="media"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)  # 媒体文件路径
