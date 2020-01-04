import logging

from django.http import JsonResponse

from lib.http import render_json
from scripts.gen_user import gen_user, show_user
from swiper.models import Swiper, Friend
from user.models import User

inf_log = logging.getLogger('inf')


#swiper_add，swiper_showusers应该放入user
def swiper_add(self):
    gen_user(100)
    return render_json('添加用户成功')

def swiper_showusers(self):
    users = show_user()

    showuser = []
    for user in users:
        showuser.append({
            'id': user.id,
            'nikename': user.nickname,
            'gender': user.gender,
            'location': user.location,
            'avatar': user.avatar  if user.avatar else ''
        })
    # 返回数据
    return JsonResponse(showuser, safe=False)


def swiper_users(request):
    # 0.准备一个要排除的用户id
    swipered_users = []
    swiper = Swiper.objects.filter(source_id = request.user.id).only('target_id')
    for swp in swiper:
        swipered_users.append(swp.target_id)
    #把自己放进入
    swipered_users.append(request.user.id)

    #暂时未使用推荐算法
    users = User.objects.filter().exclude(id__in = swipered_users)[:20]
    # TODO:未来用suprise算法

    res_user = []
    for user  in users:
        res_user.append(user.to_dict())

    return render_json(res_user)
    # 1.取出可滑动用户

    # 2.取出滑过的用户
    # 3.去掉自己

#
def swiper_like(request):
    target_id = int(request.POST.get('target_id'))
    source_id = request.user.id

    Swiper.swipe('like',source_id, target_id)
    if Swiper.is_liked_someone(source_id, target_id):
        # 建立好友关系
        # 类方法
        Friend.make_friends(target_id, source_id)
        # TODO: 向好友推送完成匹配的消息 (集成消息推送服务)
        # 1. 应用内消息通知，只有当接收消息的人打开app的时候才能看到
        # 2. 消息推送的方式，把消息push到用户手机的通知栏
        #   a. iOS 只有一种做法：调用苹果的Push Notification服务
        #   b. Android 有两种做法：
        #     i. 自己写一个Android的后台服务，跟自己的服务器建立长链接，有消息推过来就提示用户
        #     ii. 集成第三方的消息推送服务，它自己肯定也有一个Android后台服务活着，跟他的服务器通信

        return True  # 返回完成匹配的结果
    else:
        return False
