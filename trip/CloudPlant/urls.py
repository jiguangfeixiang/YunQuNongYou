from django.urls import path

from trip.CloudPlant import User, MyPlant, MyPlantDetailAndInteraction, PlantManageRecorcd, views, message

urlpatterns = [
    path('user/<int:pk>/', User.user, name='用户界面', ),
    path('myplant/<int:pk>/', MyPlant.my_plant, name='我的作物页面'),
    # 在这里传入种植id
    path('plantdetail/<int:pk>/', MyPlantDetailAndInteraction.plant_detail, name='种植详情'),
    path('plantrecord/<int:pk>/', PlantManageRecorcd.manage_record, name='种植记录和互动见面'),
    # 传入记录id
    path('taskcare/handler/', views.task_handler, name='养护任务处理'),
    # 获取所有作物的信息
    path('croplist/<int:user_id>', views.crop_list, name='获取所有作物信息'),
    # 作物购买情况
    path('cropbuy/', views.crop_buy, name='购买处理'),
    # 农民和用户进行通信
    path('message/usermessage/', message.user_to_former, name='用户给农民发送消息'),
    path('message/formermessage/', message.former_to_user, name='农民给用户发送消息'),
    path('message/user/<int:user_id>/', message.user_messages, name='用户的消息'),
    path('message/former/<int:former_id>/', message.former_messages, name='农民的消息'),

]
