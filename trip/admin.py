from django.contrib import admin

from .models import *

admin.site.site_title = '农业旅游管理'
admin.site.site_header = '农业旅游后台'
admin.site.index_title = '农业旅游管理'


# 产品管理
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'image', 'description', 'buy_time']
    search_fields = ['name', 'description', 'category']
    list_filter = ['name', 'description', 'category']


# 景点管理
class SceneSpotInline(admin.TabularInline):
    model = SceneSpot
    extra = 1  # 默认显示的空白内联对象数量


# 景点实地游玩内联
class ScenePlacePlayInline(admin.TabularInline):
    model = ScenePlacePlay
    extra = 1  # 默认显示的空白内联对象数量


# 景点图片管理
class SceneImageInline(admin.TabularInline):
    model = SceneImage
    extra = 1  # 默认显示的空白内联对象数量


# 景点评论管理
class SceneCommentInline(admin.TabularInline):
    model = SceneComment
    extra = 1  # 默认显示的空白内联对象数量


# 省份管理
@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    inlines = [SceneSpotInline]
    list_display = ['id', 'name', ]
    search_fields = ['id', 'name', ]
    list_filter = ['id', 'name', ]


# 景点食物
class SceneFoodInline(admin.TabularInline):
    model = SceneFood
    extra = 1  # 默认显示的空白内联对象数量


# 景点游玩活动
class SceneActivityInline(admin.TabularInline):
    model = SceneActivity
    extra = 1  # 默认显示的空白内联对象数量


# 景点云种植项目
class SceneProjectInline(admin.TabularInline):
    model = ScenePlantProject
    extra = 1  # 默认显示的空白内联对象数量


# 景点管理
@admin.register(SceneSpot)
class SceneSpotAdmin(admin.ModelAdmin):
    inlines = [SceneImageInline, SceneCommentInline, SceneProjectInline, ScenePlacePlayInline, SceneFoodInline,
               SceneActivityInline]
    list_display = ['id', 'name', 'description', 'visit_count', 'image', 'city']
    search_fields = ['id', 'name', 'description', 'city']
    list_filter = ['id', 'name', 'description', 'city']


# 景点管理

# 景点管理
# 用户
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'create_time', 'avatar']
    search_fields = ['id', 'username']
    list_filter = ['id', 'username', ]


# # 项目
# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'project_type', 'description', 'price', 'quantity', 'trip_day', 'start_time']
#     search_fields = ['id', 'name', 'start_time']
#     list_filter = ['id', 'name', 'start_time']
#

# 订单
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'status', 'create_time', 'user', 'product', 'formers']
#     search_fields = ['status', 'user__username', 'product__name']
#     list_filter = ['status', 'create_time']

# 内联作物基本信息的图片
class CropInfoImageInline(admin.TabularInline):
    model = CropInfoImage
    extra = 1  # 默认显示的空白内联对象数量


# 作物基本信息
@admin.register(CropInfo)
class CropInfoAdmin(admin.ModelAdmin):
    inlines = [CropInfoImageInline]
    list_display = ['id', 'name', 'choice', 'growth_area', 'state', 'growth_cycle', 'purpose', 'environment',
                    'mature_day']
    search_fields = ['name', 'choice', 'sowing_season']
    list_filter = ['choice', 'sowing_season', 'growth_cycle']


#
# # 作物基本信息的图片
# @admin.register(CropInfoImage)
# class CropInfoImageAdmin(admin.ModelAdmin):
#     list_display = ['id', 'image', 'crop_info']
#     search_fields = ['crop_info__name']
#     list_filter = ['crop_info__name']


# 内联一个用户拥有作物的图片
class OwnedCropImageInline(admin.TabularInline):
    model = OwnedCropImage
    extra = 1  # 默认显示的空白内联对象数量


# 给记录内联一个生长记录
class OwnedCropRecordInline(admin.TabularInline):
    model = GrowRecord
    extra = 1


# 给记录内联一个事件
class OwnedCropEventInline(admin.TabularInline):
    model = EventRecord
    extra = 1


# 给记录内联一个任务关心
# class OwnedCropCareTaskInline(admin.TabularInline):
#     model = CropCareTask
#     extra = 1

# 给拥有作物内联一个轮播图
# 用户拥有作物的信息


@admin.register(OwnedCrop)
class OwnedCropAdmin(admin.ModelAdmin):
    inlines = [OwnedCropImageInline, OwnedCropRecordInline, OwnedCropEventInline, ]
    list_display = ['id', 'get_crop_name', 'get_crop_username', 'buy_date', 'growth_stage', 'plant_day', 'owner']
    search_fields = ['owner__username', 'growth_stage', ]
    list_filter = ['growth_stage', 'buy_date']

    # 通知展示作物的用户和作物的基本信息
    def get_crop_name(self, obj):
        return obj.crop_info.name

    get_crop_name.short_description = '作物名称'

    def get_crop_username(self, obj):
        return obj.owner.username

    get_crop_username.short_description = '作物拥有者'


# 给生长记录内联图片
class GrowRecordImageInline(admin.TabularInline):
    model = GrowRecordImage
    extra = 1  # 默认显示的空白内联对象数量


# 给事件记录内联图片
# 生长记录
@admin.register(GrowRecord)
class GrowRecordAdmin(admin.ModelAdmin):
    inlines = [GrowRecordImageInline]
    list_display = ['id', 'record_date', 'get_owned_crop_name', 'tips', 'get_owned_user', 'owned_crop', 'temperature',
                    'air_humidity',
                    'soil_ph', 'soil_moisture', 'pest_status', 'co2_level']
    search_fields = ['id', 'owned_crop__owner__username', 'owned_crop__crop_info__name', 'record_date']
    list_filter = ['weather', 'record_date']
    # 设置只读字段和关联字段的信息,只读字段是当天记录的时期,关联字段是用户的名字和拥有作物的名字,搜索字段用__
    readonly_fields = ['tips', ]

    # 获取购买者
    def get_owned_user(self, obj):
        if obj.owned_crop:
            return obj.owned_crop.owner.username

    get_owned_user.short_description = '购买者'

    # 展示生长记录的拥有作物名字,get是展示的也就是display
    def get_owned_crop_name(self, obj):
        if obj.owned_crop:
            return obj.owned_crop.crop_info.name
        return "无"

    get_owned_crop_name.short_description = '拥有作物名称'

    def tips(self, obj):
        if obj.owned_crop and obj.owned_crop.crop_info:
            date = obj.record_date.strftime('%Y-%m-%d')
            former = obj.owned_crop.crop_info.former.username
            crop_name = obj.owned_crop.crop_info.name
            msg = f'{former}在{date}这天记录一个{crop_name}的生长情况'
            return msg
        return "相关作物信息不完整"

    tips.short_description = '提示信息'


# 内联作物信息
class CropInfoInline(admin.TabularInline):
    model = CropInfo


# 农民
@admin.register(Former)
class FormerAdmin(admin.ModelAdmin):
    inlines = [CropInfoInline]
    list_display = ['id', 'nickname', 'username', 'phone', 'bio']
    # search_fields = ['user__username']
    # list_filter = ['user__username']


# 农民和用户之间的消息
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'if_read', 'time', 'sender_user', 'receiver_former', 'content', 'sender_former',
                    'sender_user']
