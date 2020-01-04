import logging

from django.core.cache import cache
from common.keys import VCODE_PREFIX
from lib.http import render_json
from lib.sms import send_sms
from social import settings
from user.logics import upload_qiniu
from user.models import User
#写入 info.log 文件
inf_log = logging.getLogger('inf')

#写入 控制台
inf_log = logging.getLogger('django')

#先经过 Session 中间件的process_request
def user_phone(request):
    '''提交手机号，发送验证码'''
    phone = request.POST.get('phone')
    # phone = request.GET.get('phone')
    print(phone)
    send_sms(phone)

    #return 之后会经过Session 中间件的process_response
    return render_json(None)


def user_vcode(request):
    '''验证验证码'''
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')

    print(f'接收的phone: {phone}')
    print(f'接收的vcode: {vcode}')
    return render_json(verify_vcode(phone, vcode,request))


def verify_vcode(phone, vcode,request):
    # 取出缓存里保存的 vcode
    VCODE = VCODE_PREFIX
    server_vcode = cache.get(f'{VCODE}{phone}')

    print(f'server_vcode type:{type(server_vcode)}')
    print(f'vcode type:{type(vcode)}')

    # 比对两个 vocde 是否一致
    if str(server_vcode) == str(vcode):
        # 一致则让用户登录
        # get_or_create 返回的结构是一个 tuple，我们为了解包，用了 user, _
        user, _ = User.objects.get_or_create(phone=phone, nickname=phone)
        #使用session
        request.session['uid'] = user.id
        #
        # inf_log.info(f'login {user.id}')  # 日志记录
        inf_log.info('login ' + str(user.id))  # 日志记录
        return user.to_dict()
    else:
        # 不一致则让用户重新登录:
        inf_log.info('验证码填写错误 ')   # 日志记录
        return {'vcode':10001}

#获取信息
def user_profile(request):
    # user_id = request.session['uid']
    # user = User.objects.get(id = user_id)
    return   render_json(request.user.to_dict())

#上传图片
def user_avatar(request):
    #1.存下来
    # 定义上传后保存的文件名
    file_name =f'avatar-{request.user.id}.jpg'
    # 上传后保存的路径
    file_path = f'{settings.BASE_DIR}/static/{file_name}'
    #接收上传文件内容
    f = request.FILES['avatar']

    with open(file_path,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    print('save local ok.')
    user_id = request.user.id
    #delay很重要！！！
    upload_qiniu.delay(file_name, file_path, user_id)
    return  render_json('已经放入celery-redis队列中')

