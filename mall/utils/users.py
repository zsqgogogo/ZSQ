from django.contrib.auth.backends import ModelBackend
#登陆
# 后端接口设计：
# 请求方式： POST /users/auths/
# 请求参数：
# 参数名 	类型 	说明
# username 	str 	用户名
# password 	str 	密码
#
# 返回数据：
# 返回值 	类型 	说明
# username 	str 	用户名
# user_id 	int 	用户id
# token 	str 	身份认证凭据
import re

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'username':user.username,
        'user_id':user.id,
        'token':token
    }

class UsernameMobileModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if re.match(r'^1[3-9]\d{9}',username):
                user=User.objects.get(mobile=username)
            else:
                user=User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user is not None and user.check_password(password):
            return user
