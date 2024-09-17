import datetime

from django.db import models


# 6个
# Create your models here.
# 景点模型
# 省
class Province(models.Model):
    name = models.CharField(max_length=100, verbose_name='省份名称')

    # 关系字段
    class Meta:
        verbose_name = '省份'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SceneSpot(models.Model):
    name = models.CharField(max_length=100, verbose_name='景点名称')
    description = models.CharField(max_length=300, verbose_name='景点描述', blank=True, null=True)
    visit_count = models.IntegerField(default=0, verbose_name='访问次数')
    image = models.ImageField(upload_to='SceneImage', verbose_name='景点图片', blank=True, null=True)
    geography_map = models.ImageField(upload_to='geography_map', verbose_name='景点地图', blank=True, null=True)
    background_video = models.FileField(upload_to='video/background_video', verbose_name='背景视频', blank=True,
                                        null=True)
    city = models.CharField(max_length=100, verbose_name='所在城市', db_index=True)

    # 关系字段
    belong_province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name='省份',
                                        related_name='scene_spots')

    class Meta:
        verbose_name = '景点详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SceneImage(models.Model):
    image = models.ImageField(upload_to='SceneImage', verbose_name='景点图片', blank=True, null=True)
    # 关系字段
    scene_spot = models.ForeignKey(SceneSpot, on_delete=models.CASCADE, verbose_name='景点',
                                   related_name='scene_images')


# 当地景点特产
class SceneFood(models.Model):
    name = models.CharField(max_length=100, verbose_name='特产名称')
    title = models.CharField(max_length=100, verbose_name='特产标题', )
    time = models.DateTimeField(auto_now_add=True, verbose_name='特产发布时间')
    description = models.CharField(max_length=300, verbose_name='特产描述')
    image = models.ImageField(upload_to='SceneFoodImage', verbose_name='特产图片', )
    image_detail = models.ImageField(upload_to='SceneFoodImage', verbose_name='特产图片详情', )
    # 关系字段
    scene_spot = models.ForeignKey(SceneSpot, on_delete=models.CASCADE, verbose_name='特产关联的景点',
                                   related_name='scene_foods')

    def __str__(self):
        return self.name


# 景点游玩活动
class SceneActivity(models.Model):
    # CHOICES = (
    #     ('drive', '自驾游'),
    #     ('team', '拼团队游'),
    # )
    name = models.CharField(max_length=100, verbose_name='活动名称')
    title = models.CharField(max_length=100, verbose_name='活动标题', )
    # types = models.CharField(max_length=10, choices=CHOICES, verbose_name='项目类型', blank=True, null=True)
    # count = models.IntegerField(default=0, verbose_name='项目数量')
    time = models.DateTimeField(auto_now_add=True, verbose_name='活动发布时间')
    description = models.CharField(max_length=300, verbose_name='活动描述')
    image = models.ImageField(upload_to='SceneActivityImage', verbose_name='活动图片')
    detail_image = models.ImageField(upload_to='SceneActivityImage', verbose_name='活动图片详情', )
    # 关系字段
    scene_spot = models.ForeignKey(SceneSpot, on_delete=models.CASCADE, verbose_name='活动关联的景点',
                                   related_name='scene_activities')

    def __str__(self):
        return self.name


# 景点云种植项目
class ScenePlantProject(models.Model):
    name = models.CharField(max_length=100, verbose_name='云种植项目名称')
    title = models.CharField(max_length=100, verbose_name='云种植项目标题', )
    image = models.ImageField(upload_to='SceneCloudPlantImage', verbose_name='云种植项目图片', blank=True)
    introduce1 = models.CharField(max_length=20, verbose_name='云种植介绍1', default='无')
    introduce2 = models.CharField(max_length=20, verbose_name='云种植介绍2', default='无')
    introduce3 = models.CharField(max_length=20, verbose_name='云种植介绍3', default='无')
    introduce4 = models.CharField(max_length=20, verbose_name='云种植介绍4', default='无')
    time = models.DateTimeField(auto_now_add=True, verbose_name='云种植项目发布时间')
    # 关系字段
    scene_spot = models.OneToOneField(SceneSpot, on_delete=models.CASCADE, verbose_name='景点关联的云种植项目',
                                      related_name='plant')


# 景点实地游玩
class ScenePlacePlay(models.Model):
    name = models.CharField(max_length=100, verbose_name='实地游玩项目名称')
    title = models.CharField(max_length=100, verbose_name='实地游玩项目标题', )
    image = models.ImageField(upload_to='ScenePlacePlay', verbose_name='实地游玩项目图片', blank=True, null=True)
    introduce1 = models.CharField(max_length=20, verbose_name='实地游玩介绍1', default='无')
    introduce2 = models.CharField(max_length=20, verbose_name='实地游玩介绍2', default='无')
    introduce3 = models.CharField(max_length=20, verbose_name='实地游玩介绍3', default='无')
    introduce4 = models.CharField(max_length=20, verbose_name='实地游玩介绍4', default='无')
    time = models.DateTimeField(auto_now_add=True, verbose_name='实地游玩项目发布时间')
    # 关系字段
    scene_spot = models.OneToOneField(SceneSpot, on_delete=models.CASCADE, verbose_name='景点关联的实地游玩项目',
                                      related_name='place_play')


class Project(models.Model):
    PROJECT_TYPE_CHOICES = (
        ('Plant', '云种植'),
        ('Tour', '实地游玩')
    )
    name = models.CharField(max_length=100, verbose_name='项目名称')
    description = models.CharField(max_length=300, verbose_name='项目描述', blank=True, null=True)
    image = models.ImageField(upload_to='ProjectImage', verbose_name='项目图片', blank=True, null=True)
    project_type = models.CharField(max_length=10, choices=PROJECT_TYPE_CHOICES, verbose_name='项目类型')
    quantity = models.IntegerField(default=0, verbose_name='项目数量')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='项目价格', default=0)
    trip_day = models.IntegerField(default=0, verbose_name='游玩天数')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='项目开始时间')
    start_place = models.CharField(max_length=100, verbose_name='项目起点', blank=True, null=True)

    destination = models.CharField(max_length=100, verbose_name='项目目的地', blank=True, null=True)
    # 关系字段
    scene_spot = models.ForeignKey(SceneSpot, on_delete=models.CASCADE, verbose_name='项目关联的景点',
                                   related_name='projects')

    class Meta:
        verbose_name = '景点项目'
        verbose_name_plural = '景点项目'

    def __str__(self):
        return self.name


# 用户
class User(models.Model):
    GENDER_CHOICES = (
        ('M', '男性'),
        ('F', '女性'),
        ('O', '其他'),
    )
    username = models.CharField(max_length=100, verbose_name='用户名')
    password = models.CharField(max_length=100, verbose_name='密码')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name='性别')
    phone = models.CharField(max_length=11, verbose_name='手机号', blank=True, null=True)
    nickname = models.CharField(max_length=10, blank=True, null=True, verbose_name='昵称')
    avatar = models.ImageField(upload_to='avatar', verbose_name='头像', blank=True, null=True)
    bio = models.CharField(max_length=300, verbose_name='简介', blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = '用户管理'

    def __str__(self):
        return self.username


class SceneComment(models.Model):
    content = models.CharField(max_length=300, verbose_name='评论内容')
    image = models.ImageField(upload_to='CommentImage', verbose_name='评论图片', blank=True, null=True)
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    business_comment = models.CharField(max_length=300, verbose_name='商家评论', blank=True, null=True)
    rating = models.IntegerField(default=0, verbose_name='用户评分')
    # 关系字段
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', related_name='comments')
    scene_spot = models.ForeignKey(SceneSpot, on_delete=models.CASCADE, verbose_name='所属景点',
                                   related_name='comments')


# 产品
class Product(models.Model):
    CATEGORY_CHOICES = (
        ('fruit', '水果'),
        ('vegetable', '蔬菜'),
        ('animal', '禽类'),
    )
    name = models.CharField(max_length=100, verbose_name='产品名称')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, verbose_name='产品类别')
    description = models.CharField(max_length=300, verbose_name='产品描述')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='产品价格')
    image = models.ImageField(upload_to='ProductImage', verbose_name='产品图片')
    buy_time = models.DateTimeField(auto_now_add=True, verbose_name='购买时间')
    # 关系字段
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='拥有者',
                              related_name='product')

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'

    def __str__(self):
        return self.name


# 农民
class Former(models.Model):
    # 用户
    GENDER_CHOICES = (
        ('M', '男性'),
        ('F', '女性'),
        ('O', '其他'),
    )
    username = models.CharField(max_length=100, verbose_name='用户名')
    password = models.CharField(max_length=100, verbose_name='密码')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name='性别')
    phone = models.CharField(max_length=11, verbose_name='手机号', blank=True, null=True, default='123')
    area = models.CharField(max_length=50, blank=True, null=True, verbose_name='所在地区', default='无')
    nickname = models.CharField(max_length=10, blank=True, null=True, verbose_name='昵称')
    avatar = models.ImageField(upload_to='avatar', verbose_name='头像', blank=True, null=True)
    bio = models.CharField(max_length=300, verbose_name='简介', blank=True, null=True)
    create_time = models.DateTimeField(default=datetime.datetime.now(), verbose_name='创建时间', )

    class Meta:
        verbose_name = '农民管理'
        verbose_name_plural = '农民管理'

    # 关系字段
    # user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='农民的用户', related_name='formers')
    def __str__(self):
        return self.username


# 订单
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('confirmed', '已确认'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
        ('cancelled', '已取消'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='订单创建时间')
    # 关系字段
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='订单的用户', related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='订单所属产品')
    former = models.ForeignKey(Former, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='订单卖家')


# # 自定义CropInfo模型方法
# class CropInfoManager(models.Manager):
#     def month_within(self):
#         return self.filter(growth_cycle__lte=30)
#
#     def one_to_three_month(self):
#         return self.filter(grow_cycle__lte=90, growth_cycle__gt=30)
#
#     def three_to_six_month(self):
#         return self.filter(grow_cycle__lte=180, growth_cycle__gt=90)
#
#     def six_to_twelve_month(self):
#         return self.filter(grow_cycle__lte=360, growth_cycle__gt=180)
#
#     def more_than_twelve_month(self):
#         return self.filter(growth__cycle__gt=360)


# 作物的基本信息
class CropInfo(models.Model):
    BASE_CHOICE = (
        ('vegetable', '蔬菜'),
        ('fruit', '水果'),
    )
    SEASON_CHOICE = (
        ('spring', '春'),
        ('summer', '夏'),
        ('autumn', '秋'),
        ('winter', '冬'),
    )
    PURPOSE_CHOICE = (
        ('edible', '食用'),
        ('watch', '观赏'),
    )
    ENVIRONMENT_CHOICE = (
        ('indoor', '室内'),
        ('outdoor', '室外'),
    )
    BUY_STATE_CHOICE = (
        ('purchased', '已购买'),
        ('purchase', '未购买'),
    )
    name = models.CharField(max_length=100, verbose_name='作物名称')
    choice = models.CharField(max_length=10, choices=BASE_CHOICE, verbose_name='作物类型')
    growth_area = models.CharField(max_length=100, verbose_name='生长区域', blank=True, null=True)
    city = models.CharField(max_length=20, verbose_name='种植的城市', default='必填的城市')
    sowing_season = models.CharField(max_length=10, choices=SEASON_CHOICE, verbose_name='播种季节', blank=True,
                                     null=True)
    state = models.CharField(max_length=10, choices=BUY_STATE_CHOICE, verbose_name='购买状态', blank=True, null=True,
                             default='purchase')
    growth_cycle = models.IntegerField(default=0, verbose_name='生长周期', blank=True, null=True)
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICE, verbose_name='作物用途', blank=True, null=True)
    environment = models.CharField(max_length=10, choices=ENVIRONMENT_CHOICE, verbose_name='生长环境', blank=True,
                                   null=True)
    mature_day = models.IntegerField(default=0, verbose_name='成熟日期')
    image = models.ImageField(upload_to='CropInfoImage', verbose_name='作物图片', blank=True, null=True)
    description = models.CharField(max_length=300, verbose_name='作物描述', blank=True, null=True)
    q_image = models.ImageField(upload_to='CropInfoQImage', verbose_name='作物Q版萌图', blank=True, null=True)
    # 生长周期管理器
    # object = CropInfoManager()
    # 关系字段
    former = models.ForeignKey(Former, on_delete=models.CASCADE, verbose_name='关联的农民')
    scene_spot = models.ManyToManyField(SceneSpot, blank=True, null=True, verbose_name='作物所属景点',
                                        related_name='crop_info')

    class Meta:
        verbose_name = '作物基本信息'
        verbose_name_plural = '作物基本信息'

    def __str__(self):
        return self.name


def __str__(self):
    return self.name


# 作物基本信息的图片
class CropInfoImage(models.Model):
    image = models.ImageField(upload_to='CropInfoImage', verbose_name='作物图片', blank=True, null=True)
    # 设置关系字段
    crop_info = models.ForeignKey(CropInfo, on_delete=models.CASCADE, verbose_name='作物基本信息',
                                  related_name='images')

    class Meta:
        verbose_name = '作物详情照片'
        verbose_name_plural = "作物详情照片"


# 用户拥有的作物模型
class OwnedCrop(models.Model):
    GROWTH_STAGE_CHOICES = (
        ('germination', '发芽期'),
        ('seedling', '幼苗期'),
        ('planting', '生长期'),
        ('flower_and_fruiting', '开花结果期'),
        ('mature', '成熟期'),
        ('harvest', '采收期'),

    )
    buy_date = models.DateTimeField(auto_now_add=True, verbose_name='购买日期')
    growth_stage = models.CharField(max_length=100, choices=GROWTH_STAGE_CHOICES)
    plant_day = models.IntegerField(default=0, verbose_name='种植天数')
    image = models.ImageField(upload_to='OwnedCropImage', verbose_name='作物图片', blank=True, null=True)
    # 关系字段
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='用户的作物', related_name='owned_crops')
    crop_info = models.OneToOneField(CropInfo, on_delete=models.CASCADE, verbose_name='作物的基本信息',
                                     related_name='owned_crops')

    # 每次添加拥有作物之后就要添加一条作物信息的当天记录
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new:
            super(OwnedCrop, self).save(*args, **kwargs)  # 先保存OwnedCrop实例
            try:
                GrowRecord.objects.create(owned_crop=self, record_date=datetime.date.today())
                print('作物信息记录创建成功')
            except Exception as e:
                print("作物信息创建记录的保存过程中出现错误：", str(e))
        else:
            super(OwnedCrop, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '用户拥有的作物'
        verbose_name_plural = "用户拥有的作物"

    def __str__(self):
        try:
            name = self.crop_info.name
        except:
            name = '未知'
        return name


# 用户拥有单个作物的多个图片
class OwnedCropImage(models.Model):
    image = models.ImageField(upload_to='OwnedCropImage', verbose_name='作物图片', blank=True, null=True)
    # 设置关系字段
    owned_crop = models.ForeignKey(OwnedCrop, on_delete=models.CASCADE, verbose_name='用户的作物',
                                   related_name='images')

    class Meta:
        verbose_name = '轮播图详情照片'
        verbose_name_plural = "轮播图详情照片"

    # def upload_to(instance):


#     today = datetime.datetime.now().strftime('%Y-%m-%d')
#     own_crop_name = instance.owned_crop.name
#     user_name = instance.owner.owned_crops.owner.username
#     return f'{user_name}/{own_crop_name}/{today}/'


# 作物的一天生长记录模型
class GrowRecord(models.Model):
    PEST_STATUS_CHOICES = (
        ('healthy', '健康'),
        ('poisonous', '少量害虫骚扰'),
        ('dangerous', '危险'),
        ('dead', '死亡'),
        ('unknown', '未知'),
    )
    COLOR_CHOICES = (
        ('green', '绿色'),
        ('yellow', '黄色'),
        ('red', '红色'),
        ('black', '黑色'),
        ('white', '白色')
    )
    weather = models.CharField(max_length=10, verbose_name='天气状况', blank=True, null=True)
    record_date = models.DateField(verbose_name='记录日期')
    temperature = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='天气温度', default=0)
    temperature_color = models.CharField(max_length=10, choices=COLOR_CHOICES, verbose_name='天气温度颜色',
                                         default='green')
    air_humidity = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='空气湿度', default=0)
    air_humidity_color = models.CharField(max_length=10, choices=COLOR_CHOICES, verbose_name='空气湿度颜色',
                                          default='green')
    soil_ph = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='土壤酸碱性', default=0)
    soil_ph_color = models.CharField(max_length=10, choices=COLOR_CHOICES, verbose_name='土壤酸碱性颜色',
                                     default='green')
    soil_moisture = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='土壤湿度', default=0)
    soil_moisture_color = models.CharField(max_length=10, choices=COLOR_CHOICES, verbose_name='土壤湿度颜色',
                                           default='green')
    pest_status = models.CharField(max_length=10, choices=PEST_STATUS_CHOICES, verbose_name='病虫害状态',
                                   default='healthy')
    co2_level = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='当前作物的二氧化碳浓度', default=0)
    co2_level_color = models.CharField(max_length=10, choices=COLOR_CHOICES, verbose_name='当前作物的二氧化碳浓度颜色',
                                       default='green')
    photo_morning = models.ImageField(upload_to='record_morning', verbose_name='早晨照片', blank=True, null=True)
    photo_noon = models.ImageField(upload_to='record_noon', verbose_name='中午照片', blank=True, null=True)
    photo_evening = models.ImageField(upload_to='record_evening', verbose_name='晚上照片', blank=True, null=True)
    growth_height = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='生长高度', default=0.00)
    growth_speed = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='生长速度', default=0.00)
    # 关系字段
    owned_crop = models.ForeignKey(OwnedCrop, on_delete=models.CASCADE, verbose_name='被记录的作物',
                                   related_name='records')

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        print(f'记录创建是{is_new},准备创建养护任务')
        try:
            super(GrowRecord, self).save(*args, **kwargs)
            if is_new:
                CropCareTask.objects.create(record=self)
                print('记录的任务养护创建成功')
        except Exception as e:
            print("保存过程中出现错误：", str(e))

    class Meta:
        # unique_together = ('record_date', 'owned_crop')
        db_table = 'trip_growrecord'
        verbose_name = '生长记录'
        verbose_name_plural = '生长记录'


# 一天生长记录的照片
class GrowRecordImage(models.Model):
    image = models.ImageField(upload_to='GrowRecordImage', verbose_name='照片', blank=True, null=True)
    # 设置关系字段
    grow_record = models.ForeignKey(GrowRecord, on_delete=models.CASCADE, verbose_name='生长记录',
                                    related_name='images')

    def __str__(self):
        return str(self.grow_record.owned_crop.crop_info.name)


# 农作物养护任务模型
class CropCareTask(models.Model):
    # TASK_CHOICE = (
    #     ('water', '浇水'),
    #     ('fertilize', '施肥'),
    #     ('weed', '除草'),
    # )
    task_date = models.DateTimeField(auto_now_add=True, verbose_name='任务建立日期')
    task_water = models.CharField(max_length=10, default="浇水", verbose_name='浇水')
    task_fertilize = models.CharField(max_length=10, default="施肥", verbose_name='施肥')
    task_weed = models.CharField(max_length=10, default="除草", verbose_name='除草')
    task_pest = models.BooleanField(default=False, verbose_name='害虫', blank=True, null=True)
    # task_type = models.CharField(max_length=20, choices=TASK_CHOICE, verbose_name='任务类型')
    water_count = models.IntegerField(default=0, verbose_name='浇水次数', blank=True, null=True)
    fertilize_count = models.IntegerField(default=0, verbose_name='施肥次数', blank=True, null=True)
    weed_count = models.IntegerField(default=0, verbose_name='除草次数', blank=True, null=True)
    # 关系字段
    record = models.OneToOneField(GrowRecord, on_delete=models.CASCADE, related_name='care_task')


# 事件媒体记录模型
class EventRecord(models.Model):
    event_date = models.DateTimeField(auto_now_add=True, verbose_name='事件时间')
    event_type = models.CharField(max_length=100, verbose_name='事件类型')
    description = models.CharField(max_length=300, verbose_name='事件描述', blank=True, null=True)
    # 关系字段
    owner_crop = models.ForeignKey(OwnedCrop, on_delete=models.CASCADE, related_name='event_record')


# 用户操作历史模型
class UserOperationHistory(models.Model):
    action_date = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    action_type = models.CharField(max_length=100, verbose_name='操作类型')
    description = models.CharField(max_length=300, verbose_name='操作内容', blank=True, null=True)
    # 关系字段
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户的操作历史',
                             related_name='action_history', )


class testImage(models.Model):
    image = models.ImageField(verbose_name='图片上传测试', upload_to='testImage', blank=True, null=True)


# 用户和农合发送消息模型
class Message(models.Model):
    time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')
    content = models.TextField()
    if_read = models.BooleanField(default=False, verbose_name='是否已读')
    # 关系字段
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户发送',
                                    related_name='send_message', blank=True, null=True)
    sender_former = models.ForeignKey(Former, on_delete=models.CASCADE, verbose_name='农户发送',
                                      related_name='send_message', blank=True, null=True)
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户接收',
                                      related_name='receive_message', blank=True, null=True)
    receiver_former = models.ForeignKey(Former, on_delete=models.CASCADE, verbose_name='农户接收',
                                        related_name='receive_message', blank=True, null=True)

    class Meta:
        verbose_name = '聊天记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        # 判断四个哪两个有值
        if self.sender_user and self.receiver_former:
            return self.sender_user.username + '->' + self.receiver_former.username
        elif self.sender_former and self.receiver_user:
            return self.sender_former.username + '->' + self.receiver_user.username
        else:
            return '无'
