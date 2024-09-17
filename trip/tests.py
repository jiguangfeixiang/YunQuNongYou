import faker
from faker import Faker
from trip.models import Province
fake = Faker()

# 生成省份数据
province_names = [
    "北京", "天津", "上海", "重庆",
    "河北", "山西", "辽宁", "吉林", "黑龙江",
    "江苏", "浙江", "安徽", "福建", "江西", "山东",
    "河南", "湖北", "湖南", "广东", "海南",
    "四川", "贵州", "云南", "陕西", "甘肃", "青海",
    "台湾",
    "内蒙古自治区", "广西壮族自治区", "西藏自治区", "宁夏回族自治区", "新疆维吾尔自治区",
    "香港特别行政区", "澳门特别行政区"
]
for name in province_names:
    province = Province(name=name)
    province.save()
#     faker.
# 生成景点数据
# provinces = Province.objects.all()
# for _ in range(50):  # 生成50个景点
#     spot = SceneSpot(
#         name=fake.city(),
#         description=fake.text(max_nb_chars=200),
#         visit_count=random.randint(0, 1000),
#         province=random.choice(provinces)
#     )
#     spot.save()
# #
# # from trip.models import User
# # from faker import Faker
# # import random
# #
# # fake = Faker('zh_CN')
# #
# # # 生成用户数据
# # for _ in range(20):  # 假设我们要生成20个用户
# #     user = User(
# #         username=fake.user_name(),
# #         password=fake.password(),
# #         gender=random.choice(['M', 'F', 'O']),
# #         phone=fake.phone_number(),
# #         nickname=fake.first_name(),
# #         bio=fake.text(max_nb_chars=200),
# #         token=fake.sha256(raw_output=False),
# #         admin_token=fake.sha256(raw_output=False),
# #         # avatar 字段需要上传文件，这里我们略过
# #     )
# #     user.save()
# #     print(f"Added user: {user.username}")
# #
# # # 生成产品数据
# # users = User.objects.all()
# # categories = ['fruit', 'vegetable', 'animal']
# # for _ in range(200):  # 生成200个产品
# #     product = Product(
# #         name=fake.word(),
# #         category=random.choice(categories),
# #         description=fake.text(max_nb_chars=100),
# #         price=round(random.uniform(5.0, 100.0), 2),
# #         user=random.choice(users)
# #     )
# #     product.save()
# from trip.models import GrowRecord, OwnedCrop
#
# owned_crops = OwnedCrop.objects.all()
# if owned_crops:
#     print(owned_crops)
# else:
#     print("No owned crops available, please add some first.")
# owned_crop = owned_crops[4]  # 假设选择第一个 owned_crop
# print(owned_crop.id)
# if owned_crops:
#     try:
#         new_grow_record = GrowRecord(
#             record_date='2024-4-13',
#             temperature=20.5,
#             temperature_color='green',
#             air_humidity=30.2,
#             air_humidity_color='green',
#             soil_ph=7.0,
#             soil_ph_color='green',
#             soil_moisture=12.5,
#             soil_moisture_color='green',
#             pest_status='healthy',
#             co2_level=400.0,
#             co2_level_color='green',
#             growth_height=100.00,
#             growth_speed=1.50,
#             owned_crop=owned_crop,  # 假设选择第一个 owned_crop
#         )
#     except Exception as e:
#         print(e)
#     new_grow_record.save()
#     print("Grow record added successfully!")
