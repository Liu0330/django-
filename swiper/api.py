import logging

from scripts.gen_user import gen_user
from social import settings
from django.core.cache import cache
from lib.sms import send_sms
from lib.http import render_json
from user.logics import upload_qiniu
from user.models import User
from common.keys import VCODE_PREFIX

inf_log = logging.getLogger('inf')

def swiper_add():
    gen_user(100)
    pass
def swiper_users():
    pass

def swiper_like():
    pass
