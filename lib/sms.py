import random

import requests
from django.core.cache import cache

from common.config import SMS_SENDSMS, MOBILE_NONE_SMS
from common.keys import VCODE_PREFIX

# ucpaas发送短信api
def send_sms(phone):
    print(f"send sms: {phone}")

    # 先生成一个4位的随机验证码
    vcode = random.randrange(1000, 9999)
    print(f'真实验证码为{vcode}')
    # 保存验证码：缓存
    VCODE = VCODE_PREFIX
    cache.set(f'{VCODE}{phone}', vcode)

    # 调用发短信api，发短信
    sms_api_url = SMS_SENDSMS

    sms_params = MOBILE_NONE_SMS

    sms_params["mobile"] = phone
    sms_params["param"] = f"{vcode}, 900"

    resp = requests.post(sms_api_url, json=sms_params)

    if resp.status_code == 200:
        result_json = resp.json()
        print(result_json['code'])
        if result_json['code'] == '000000':

            return True, result_json['msg']
        else:
            return False, result_json['msg']
    else:
        return False, '短信服务器错误'

# 网易云信发送短信api
# def send_sms(phone):
#     # 获取phonehttps://api.netease.im/nimserver/user/create.action
#     url = 'https://api.netease.im/sms/sendcode.action'  # 网易云信接口
#     headers = {}
#     headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
#     AppSecret = 'c6a046a10671'
#     Nonce = '111111222222333333333'
#     CurTime = str(int(time.time()))
#     headers['AppKey'] = 'e22f54f34f24eb4ddac33062d5dc880f'
#     headers['Nonce'] = Nonce
#     headers['CurTime'] = CurTime
#     s = AppSecret + Nonce + CurTime
#     headers['CheckSum'] = hashlib.sha1(s.encode('utf-8')).hexdigest().lower()
#     headers['codeLen'] ='4'
#
#
#     res = requests.post(url, data={'mobile': phone}, headers=headers)
#     # post url的返回值
#     # print(res.text, type(res.text))
#     json_obj = json.loads(res.text)  # 字典
#     # print(res.text, type(res.text))
#     print(json_obj)
#     cache.set(phone, json_obj.obj)
#     # print(res.content)
#     if json_obj.code == 200:
#         return {'msg': 'ok'}
#     else:
#         return {'msg': 'fail'}