# -*- coding:utf-8 -*-
"""用户头像上传"""

import logging
from qiniu import Auth, put_data, put_file

# 需要填写你的 Access Key 和 Secret Key
ACCESS_KEY = 'q6QLur7zYpyj9rUAeUwkKA3g2BxiGRugfevdqW7r'
SECRET_KEY = 'l8AfWuWW4DfK1TrZyPzUsXc8WKa_YojUgCUG040u'

#要上传的空间
BUCKET_NAME = 'python'

# 测试图片上传文件
TEST_IAMGE_FILE = r'E:/Leeing/python/python/show-me-code/_assets/images/weixin_avatar3.png'

def storage(data):
    """七牛云存储"""

    if not data:
        return
    try:
        # #构建鉴权对象
        q = Auth(ACCESS_KEY, SECRET_KEY)

        #生成上传 Token，可以指定过期时间等
        token = q.upload_token(BUCKET_NAME)
        print(token)

        ret, info = put_data(token, None, data)
        print(ret)
        print(info)

    except Exception as e:
        logging.error(e)
        raise e
    if info and info.status_code != 200:
        raise Exception('上传文件到七牛失败')

    # 返回七牛中保存的图片名，这个图片名也是访问七牛获取图片的路径
    return ret['key']

def storage_by_file():
    """通过文件上传"""
    
    # #构建鉴权对象
    q = Auth(ACCESS_KEY, SECRET_KEY)
    #上传到七牛后保存的文件名
    key = 'my-flask-logo.png'
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(BUCKET_NAME, key, 3600)
    #要上传文件的本地路径
    localfile = TEST_IAMGE_FILE
    ret, info = put_file(token, key, localfile)
    print(ret)
    print(info.status_code)
    return ret['key']

def main():
    with open(, 'rb') as f:
        data = f.read()
        url = storage(data)
        print(url)

if __name__ == '__main__':
    main()