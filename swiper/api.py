import logging

from django.http import JsonResponse

from scripts.gen_user import gen_user, show_user
from social import settings
from django.core.cache import cache
from lib.sms import send_sms
from lib.http import render_json
from user.logics import upload_qiniu
from user.models import User
from common.keys import VCODE_PREFIX

inf_log = logging.getLogger('inf')

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




def swiper_users():
    pass

def swiper_like():
    pass
