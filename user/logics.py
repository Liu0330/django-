# -*- coding: utf-8 -*-
from qiniu import Auth, put_file, etag

from user.models import User
from worker import celery_app

#引入work中celery_app，调用异步
@celery_app.task
def upload_qiniu(file_name, file_path, user_id):
    # 2.调用七牛云sdk上传
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'KXfx2ZiBP311HkZZ8l8JHCmqlqPTJCK2sraiheVU'
    secret_key = 'pe5svTTUAJQoUPhppsf0Gg9wbEJiYahnRMAy1rgP'
    # 要上传的空间
    bucket_name = 'liu0330'
    # 要上传的域名
    bucket_domain = ' liu0330.s3-cn-south-1.qiniucs.com'
    # 构建鉴权对象
    q = Auth(access_key, secret_key, )
    token = q.upload_token(bucket_name, file_name, 3600)
    ret, info = put_file(token, file_name, file_path)
    print(info)
    #断言
    assert ret['key'] == file_name
    assert ret['hash'] == etag(file_path)
    print('save qiniu ok.')
    avatar_url = f'{bucket_domain}/{file_name}'
    # 3.更新用户的avatar
    user = User.objects.get(id=user_id)
    # user = request.user # request 无法传 所以改为user_id
    user.avatar = avatar_url
    user.save()

    return  True



