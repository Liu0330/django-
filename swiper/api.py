import logging

from django.http import JsonResponse

from common.errors import *
from lib.http import render_json
from scripts.gen_user import gen_user, show_user
from swiper.models import Swiper, Friend
from user.models import User
from vip.logics import need_perm

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
    # source_id = int(request.POST.get('source_id'))
    source_id = request.user.id

    if target_id == source_id:
        return render_json({}, '禁止喜欢自己', CODE_DISABLE_LIKE_SELF)
    Swiper.swipe('like', source_id=source_id, target_id=target_id)

    # 检查被滑动者，是否喜欢过滑动者
    if Swiper.is_liked_someone(source_id=target_id, target_id=source_id):
        Friend.make_friends(target_id, source_id)

    return render_json(None)

@need_perm('superlike')
def superlike(request):
    target_id = int(request.POST.get('target_id'))
    # source_id = int(request.POST.get('source_id'))
    source_id = request.user.id

    if target_id == source_id:
        return render_json({}, '禁止喜欢自己', CODE_DISABLE_LIKE_SELF)
    Swiper.swipe('superlike', source_id=source_id, target_id=target_id)

    # 检查被滑动者，是否喜欢过滑动者
    if Swiper.is_liked_someone(source_id=target_id, target_id=source_id):
        Friend.make_friends(target_id, source_id)

    return render_json(None)


def swiper_unlike(request):
    target_id = int(request.POST.get('target_id'))
    # source_id = int(request.POST.get('source_id'))
    source_id = request.user.id

    if target_id == source_id:
        return render_json({}, '禁止不喜欢自己', CODE_DISABLE_LIKE_SELF)
    Swiper.swipe('unlike', source_id=source_id, target_id=target_id)

    # 检查好友关系，如果是好友关系，要解除
    #if Friend.is_friend(source_id,target_id):
    Friend.break_off(source_id,target_id)

    return render_json(None)

