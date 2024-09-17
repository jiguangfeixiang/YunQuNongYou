from rest_framework import serializers

from trip.models import Product, SceneSpot, User, Province, Project, SceneComment, SceneImage, Former, Order, CropInfo, \
    OwnedCrop, GrowRecord, UserOperationHistory, EventRecord, CropCareTask, OwnedCropImage, GrowRecordImage, Message, \
    testImage, SceneFood, SceneActivity, ScenePlantProject, ScenePlacePlay


# 景点序列化器
class SceneSpotSerializer(serializers.ModelSerializer):
    # 嵌套省的这个序列化器
    belong_province = serializers.CharField(source='belong_province.name', read_only=True)

    class Meta:
        model = SceneSpot
        fields = '__all__'


# 景点实地游玩项目序列化器
class ScenePlacePlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenePlacePlay
        fields = '__all__'


# 景点图片序列化器
class SceneImageSerializer(serializers.ModelSerializer):
    scene_spot = serializers.CharField(source='scene_spot.name', read_only=True)

    class Meta:
        model = SceneImage
        fields = '__all__'


# 当地景点特产序列化器
class SceneFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = SceneFood
        fields = '__all__'


# 景点活动序列化器
class SceneActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SceneActivity
        fields = '__all__'


# 景点云种植项目
class ScenePlantProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenePlantProject
        fields = '__all__'


# 省份序列化器
class ProvinceSerializer(serializers.ModelSerializer):
    scene_spots = SceneSpotSerializer(many=True)

    class Meta:
        model = Province
        fields = '__all__'


# 如果ProvinceSerializer在前面被定义，这里需要重新定义SceneSpotSerializer以使用ProvinceSerializer

# 产品序列化器
class ProductSerializer(serializers.ModelSerializer):
    buyTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False)

    class Meta:
        model = Product
        fields = '__all__'


# 用户序列化器
class UserSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False)

    class Meta:
        model = User
        fields = '__all__'


# 项目序列化器
class ProjectSerializer(serializers.ModelSerializer):
    related_scene_spot = serializers.CharField(source='scene_spot.name', read_only=True)
    # start_time = serializers.DateTimeField(format="%Y-%m-%d", )
    user = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


# 景点评论序列化器
# 评论序列化器
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    comment_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False)
    scene_spot = serializers.CharField(source='scene_spot.name', read_only=True)

    class Meta:
        model = SceneComment
        fields = '__all__'


# 农民序列化器
class FormerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Former
        fields = '__all__'


# 订单序列化器
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


# 作物信息序列化器
class CropInfoSerializer(serializers.ModelSerializer):
    # 嵌套一个农民的自定义序列化器
    former = serializers.SerializerMethodField()
    owned_crop_id = serializers.SerializerMethodField()

    def get_owned_crop_id(self, obj):
        owned_crop = OwnedCrop.objects.filter(crop_info=obj).first()
        if owned_crop:
            return owned_crop.id
        else:
            return "抱歉,暂时这个作物还没有帅哥购买呢"

    def get_former(self, obj):
        data = {
            'former_id': obj.former.id,
            'username': obj.former.username,
            'area': obj.former.area,
            'phone': obj.former.phone,
        }
        return data

    class Meta:
        model = CropInfo
        fields = '__all__'


# 内联一个拥有作物的轮播图片
# class OwnedCropImageSerializer(serializers.):
# 用户拥有的作物模型
class OwnedCropSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    growth_stage = serializers.ChoiceField(choices=OwnedCrop.GROWTH_STAGE_CHOICES, source='get_growth_stage_display')
    growth_progress = serializers.SerializerMethodField()
    # purpose = serializers.ChoiceField(choices=OwnedCrop.crop_info.PURPOSE_CHOICE, source='get_purpose_display')
    # days_plant = serializers.SerializerMethodField()
    # if_mature = serializers.SerializerMethodField()
    former = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    owner_id = serializers.SerializerMethodField()

    def get_owner_id(self, obj):
        return obj.owner.id

    def get_image(self, obj):
        try:
            return obj.crop_info.image.url
        except:
            return f'{obj.crop_info.name}没有图片哦'

    def get_former(self, obj):
        try:
            return obj.crop_info.former.id
        except AttributeError:  # 如果 'former' 是 None 或 'crop_info' 是 None
            return None
        except CropInfo.DoesNotExist:  # 如果 'CropInfo' 实例不存在
            return None

    def get_if_mature(self, obj):
        if obj.plant_day >= obj.crop_info.mature_day:
            return True
        else:
            return False

    def get_growth_progress(self, obj):
        # Assuming obj.buy_date is already a datetime object, calculate the difference
        try:
            growth_progress = (obj.plant_day / obj.crop_info.mature_day) * 100
        except:
            growth_progress = 0
        if growth_progress > 100:
            growth_progress = 100
        return growth_progress

    class Meta:
        model = OwnedCrop
        fields = '__all__'


# 用户拥有单个作物的图片
class OwnedCropImageSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = OwnedCropImage
        fields = '__all__'


# 作物生长记录模型
class GrowRecordSerializer(serializers.ModelSerializer):
    pest_status = serializers.ChoiceField(choices=GrowRecord.PEST_STATUS_CHOICES, source='get_pest_status_display')

    class Meta:
        model = GrowRecord
        fields = '__all__'


# 生长记录的照片
class GrowRecordImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = GrowRecordImage
        fields = '__all__'


# 农作物养护任务
class CropCareTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropCareTask
        fields = '__all__'


# 事件记录序列化器
class EventRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRecord
        fields = '__all__'


# 用户操作历史模型
class UserOperationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOperationHistory
        fields = '__all__'


class testImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = testImage
        fields = '__all__'


# 消息序列化器
class MessageSerializer(serializers.ModelSerializer):
    sender_user = serializers.CharField(source='sender_user.username', read_only=True)
    sender_former = serializers.CharField(source='sender_former.username', read_only=True)
    receiver_user = serializers.CharField(source='receiver_user.username', read_only=True)
    receiver_former = serializers.CharField(source='receiver_former.username', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
