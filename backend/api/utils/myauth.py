from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api import models
from datetime import datetime
from rest_framework.response import Response

# 导入项目配置文件类(用于获取秘钥, 秘钥的获取可以自定义, 不必须在此类中获取)
from django.conf import settings
# 导入加解密类
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# 自定义登录认证组件
class KennyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token=request.query_params.get('token')
        tokenobj=models.UserAuthToken.objects.filter(token=token).first()
        if not tokenobj:
            # return Response({'code':'2001','error':'用户认证失败'})
            raise AuthenticationFailed({'code':'2001','error':'用户认证失败'})
        if datetime.now().timestamp()-tokenobj.created_or_updated.timestamp() > 259200:
            # return Response({'code': '2001', 'error': '用户认证已过期，请重新登录'})
            raise AuthenticationFailed({'code': '2001', 'error': '用户认证已过期，请重新登录'})
        # 认证时更新token时间，从而使到期时间不是固定的三天
        tokenobj.save()
        return (tokenobj.user,token)

# 自定义登录认证组件2，只为了返回当前user
class KennyAuthenticationForUser(BaseAuthentication):
    def authenticate(self, request):
        token=request.query_params.get('token')
        tokenobj=models.UserAuthToken.objects.filter(token=token).first()
        # 不引发异常，只获取当前user
        if not tokenobj:
            return (None,None)
        if datetime.now().timestamp()-tokenobj.created_or_updated.timestamp() > 259200:
            return (None,None)
        # 认证时更新token时间，从而使到期时间不是固定的三天
        tokenobj.save()
        return (tokenobj.user,token)

class KennyAuthenticationForEmailBind(BaseAuthentication):
    def authenticate(self, request):
        token=request.query_params.get('token')
        serializer = Serializer(settings.SECRET_KEY, 3600)
        # 将获取到的token进行解码成res
        res = serializer.loads(token)
        # 获取用户token
        token=res['token']
        tokenobj=models.UserAuthToken.objects.filter(token=token).first()
        # 不引发异常，只获取当前user
        if not tokenobj:
            raise AuthenticationFailed({'code': '2001', 'error': '用户认证失败'})
        if datetime.now().timestamp() - tokenobj.created_or_updated.timestamp() > 259200:
            raise AuthenticationFailed({'code': '2001', 'error': '用户认证已过期，请重新登录'})
            # 认证时更新token时间，从而使到期时间不是固定的三天
        tokenobj.save()
        return (tokenobj.user, token)