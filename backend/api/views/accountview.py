from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

from api import models
from api.serializers import accountserializer
from django.http import HttpResponse
# 自定义登录认证
from api.utils.myauth import KennyAuthentication, KennyAuthenticationForEmailBind
# 分页功能
from api.utils.mypagination import MyPageNumberPagination
# 博主权限
from api.utils.mypermission import BloggerPermission
# 用于生成token
import uuid
# 使用django自带的密码加密解密类库
from django.contrib.auth.hashers import make_password, check_password
# 导入django自带的邮件类库
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
# md5加密模块
import hashlib
# 时间模块
import time
from datetime import datetime
# 引入状态码模块
from rest_framework import status
# 导入项目配置文件类(用于获取秘钥, 秘钥的获取可以自定义, 不必须在此类中获取)
from django.conf import settings
# 导入加解密类
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# 引入 Q 对象
from django.db.models import Q

# token生成函数
def md5(user):
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding="utf-8"))
    m.update(bytes(ctime, encoding="utf-8"))
    return m.hexdigest()


# 用户登录视图
class AuthView(APIView):
    """用户登录视图"""

    # 权限等级
    # permission_classes = [BloggerPermission, ]

    # 无需认证权限
    authentication_classes = []

    # serializer测试
    # def get(self,request,*args,**kwargs):
    #     user=models.Account.objects.filter(username='kenny').first()
    #     ser=AccountSerializer(instance=user,many=False)
    #     ret={
    #         "code":1000,
    #         'data':ser.data
    #     }
    #     # print(request.version)
    #     return Response(ret)

    # 运用md5生成token

    # 登录api
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000}
        username = request.data.get('username')
        user = models.Account.objects.filter(username=username).first()
        if not user:
            ret['code'] = 4004
            ret['error'] = '此用户名不存在！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        else:
            password = request.data.get('password')
            print(password)
            if not check_password(password, user.password):
                ret['code'] = 2002
                ret['error'] = '您的密码错误，请重新输入！'
                return Response(ret)
                # return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
            else:
                # 看当前用户是否存在token对象,如果存在没有超过三天，则只更新原token的过期时间，来解决无法多设备，多浏览器登录问题
                usertokenobj=models.UserAuthToken.objects.filter(user=user).first()
                if usertokenobj and datetime.now().timestamp()-usertokenobj.created_or_updated.timestamp() <= 259200:
                    usertokenobj.save()
                    token=usertokenobj.token
                else:
                    token = md5(username)
                    models.UserAuthToken.objects.update_or_create(user=user, defaults={'token': token})
                ret['data'] = {'token': token, 'userid': user.id}
                return Response(ret)

# 用户注册视图
class RegisterView(APIView):
    # 无需认证权限
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000}
        ser = accountserializer.RegisterValidateSerializer(data=request.data)
        # 可以部分更新
        # ser=RegisterValidateSerializer(data=request.data,partial=True)
        if ser.is_valid():
            try:
                ser.save()
                ret['data'] = ser.data
                return Response(ret)
            except Exception as e:
                print(e)
                ret['code'] = 2000
                ret['error'] = '用户注册失败！'
                return Response(ret)
                # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            return Response(ret)
            # return Response(ret,status=status.HTTP_400_BAD_REQUEST)


# 用户注销view
class CancelAccountView(APIView):
    authentication_classes = [KennyAuthentication, ]

    def delete(self, request, *args, **kwargs):
        ret = {'code': 1000}
        ser = accountserializer.UserGeneralInfoSerializer(instance=request.user, many=False)
        try:
            ret['data'] = ser.data
            request.user.delete()
            return Response(ret)
        except Exception as e:
            ret.pop('data')
            ret['code'] = 2000
            ret['error'] = '注销失败'
            return Response(ret)


# 用户信息展示修改视图
class UserInfoView(APIView):
    # 需要登录认证
    authentication_classes = [KennyAuthentication, ]

    def get(self, request, *args, **kwargs):
        """用户个人信息展示api"""
        ret = {'code': 1000}
        try:
            ser = accountserializer.UserInfoSerializer(instance=request.user, many=False)
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            ret['code'] = 2000
            ret['error'] = '获取个人信息失败！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        """用户个人信息修改api"""
        ret = {'code': 1000}
        ser = accountserializer.UserInfoSerializer(request.user, data=request.data, partial=True)
        if ser.is_valid():
            try:
                print(request.data)
                ser.save()
                ret['data'] = ser.data
                return Response(ret)
            except Exception as e:
                print(e)
                ret['code'] = 2000
                ret['error'] = '修改个人信息失败！'
                return Response(ret)
                # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            return Response(ret)
            # return Response(ret,status=status.HTTP_400_BAD_REQUEST)


# 用户信息粗略展示视图（非私密的，用于给他人查看个人首页的，无需登录,以及增加总点赞量、总阅读量等信息）
class UserGeneralInfoView(APIView):

    def get(self, request, *args, **kwargs):
        """用户个人中心信息展示api，用于给他人查看"""
        ret = {'code': 1000}
        pk = kwargs.get('pk')
        userobj = models.Account.objects.filter(id=pk).first()
        if not userobj:
            ret['code'] = 4004
            ret['error'] = '没有此用户！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        try:
            ser = accountserializer.UserGeneralInfoSerializer(instance=userobj, many=False)
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            print(e)
            ret['code'] = 2000
            ret['error'] = '获取个人信息失败！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 用户密码修改
class SetPasswordView(APIView):
    authentication_classes = [KennyAuthentication, ]

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000}
        if not request.user:
            ret['code'] = 2001
            ret['error'] = '您尚未登录！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
        # 原密码
        oldpassword = request.data.get('oldpassword')
        if not check_password(oldpassword, request.user.password):
            ret['code'] = 2002
            ret['error'] = '原密码输入错误'
            return Response(ret)
            # return Response(ret, status=status.HTTP_401_UNAUTHORIZED)

        ser = accountserializer.SetPasswordValidateSerializer(request.user, data=request.data)
        if ser.is_valid():
            try:
                ser.save()
                ser1 = accountserializer.AccountSerializer(instance=request.user, many=False)
                ret['data'] = ser1.data
                return Response(ret)
            except Exception as e:
                ret['code'] = 2000
                ret['error'] = '密码修改失败！'
                return Response(ret)
                # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            return Response(ret)
            # return Response(ret,status=status.HTTP_400_BAD_REQUEST)


# 用户重置密码视图1：根据邮箱发送重置密码的邮件，将token一并传送
class ResetPasswordEmailView(APIView):
    # 无需认证
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000}
        user = models.Account.objects.filter(email=request.data.get('email')).first()
        if not user:
            ret['code'] = 4004
            ret['error'] = '此用户尚未注册，请前往注册'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)

            # 获取当前token
        tokenobj = models.UserAuthToken.objects.filter(user=user).first()
        if not tokenobj:
            token = md5(user.username)
            models.UserAuthToken.objects.update_or_create(user=user, defaults={'token': token})
        else:
            tokenobj.save()
            token = tokenobj.token
        try:

            subject = '密码重置'
            # 如果有nextUrl，则根据传过来的将nextUrl连接到message中
            # 从而可以跳转之前的页面
            nexturl = request.query_params.get('nextUrl')
            print(nexturl)
            if nexturl:
                url = 'http://www.kennyeow.com/#/reset/password?token=%s&nextUrl=%s' % (token, nexturl)
            else:
                url = 'http://www.kennyeow.com/#/reset/password?token=%s' % token
            print(url)
            text_content = '请点击此链接进行密码重置:%s' % url
            html_content = '<a href=%s>请点击此链接进行密码重置</a>' % url
            from_email = 'kennyshaw@foxmail.com'
            # 默认发送text
            msg = EmailMultiAlternatives(subject, text_content, from_email, [request.data.get('email')])
            # 如果能发html,就发html
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            # send_mail(subject, message, from_email, [request.data.get('email')])
            ret['data'] = {"token": token}
            return Response(ret)
        except Exception as e:
            print(e)
            ret['code'] = 2000
            ret['error'] = '发送邮件失败'
            return Response(ret)
            # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 用户密码重置视图2，只需输入新密码即可
class ResetPasswordView(APIView):
    # 需要认证
    authentication_classes = [KennyAuthentication, ]

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000}
        # if not request.user:
        #     ret['code'] = 1001
        #     ret['error'] = '您无权修改密码！'
        # else:
        ser = accountserializer.ReSetPasswordValidateSerializer(request.user, data=request.data)
        if ser.is_valid():
            try:
                ser.save()
                ser1 = accountserializer.AccountSerializer(instance=request.user, many=False)
                ret['data'] = ser1.data
                return Response(ret)
            except Exception as e:
                ret['code'] = 2000
                ret['error'] = '密码重置失败！'
                return Response(ret)
                # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            return Response(ret)
            # return Response(ret,status=status.HTTP_400_BAD_REQUEST)


# 用户绑定邮箱视图，第一步发送邮件
class EmailBindSendView(APIView):
    authentication_classes = [KennyAuthentication, ]

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000}
        # 获取的用户token
        usertoken = request.query_params["token"]
        email = request.data.get('email')
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {"email": email, "token": usertoken}
        res = serializer.dumps(info)
        # 将用户token和邮箱合成一个加密的token进行邮件发送
        token = res.decode('utf8')
        try:

            subject = '邮箱绑定'
            url = 'http://www.kennyeow.com/#/emailbind?token=%s' % token
            text_content = '请点击此链接进行邮箱绑定:%s' % url
            html_content = '<a href=%s>请点击此链接进行邮箱绑定</a>' % url
            from_email = 'kennyshaw@foxmail.com'
            # 默认发送text
            msg = EmailMultiAlternatives(subject, text_content, from_email, [request.data.get('email')])
            # 如果能发html,就发html
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            # send_mail(subject, message, from_email, [request.data.get('email')])
            ret['data'] = token
            return Response(ret)
        except Exception as e:
            print(e)
            ret['code'] = 2000
            ret['error'] = '发送邮件失败'
            return Response(ret)


# 用户绑定邮箱视图，第二步完成绑定
class EmailBindView(APIView):
    authentication_classes = [KennyAuthenticationForEmailBind, ]

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000}
        token = request.query_params.get('token')
        serializer = Serializer(settings.SECRET_KEY, 3600)
        # 将获取到的token进行解码成res
        res = serializer.loads(token)
        email = res['email']

        try:
            request.user.email = email
            request.user.save()
            ser = accountserializer.UserInfoSerializer(instance=request.user, many=False)
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            ret['code'] = 2000
            ret['error'] = '邮箱绑定失败'
        return Response(ret)


# 用户信息管理视图
class AccountAdminView(ViewSetMixin, APIView):
    # 需要登录认证
    authentication_classes = [KennyAuthentication, ]
    # 权限等级为博主，只有博主才可进行操作
    permission_classes = [BloggerPermission, ]

    # 获取所有用户信息
    def list(self, request, *args, **kwargs):
        ret = {'code': 1000}
        text = request.query_params.get('text')
        if text:
            accounts = models.Account.objects.filter(Q(username__icontains=text) | Q(email__icontains=text)).order_by('date_joined')
        else:
            accounts = models.Account.objects.all().order_by('date_joined')
        ret['total'] = accounts.count()
        if not accounts:
            ret['code'] = 1001
            ret['error'] = '尚无用户注册！'
            return Response(ret)
        try:
            # 加入分页
            pg = MyPageNumberPagination()
            try:
                pager_accounts = pg.paginate_queryset(queryset=accounts, request=request, view=self)
            except Exception as e:
                ret['code'] = 1002
                ret['error'] = '暂无更多用户！'
                return Response(ret)
            ser = accountserializer.AccountAdminSerializer(instance=pager_accounts, many=True)
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            print(e)
            ret['code'] = 2000
            ret['error'] = '获取所有用户信息失败！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 获取某个用户的信息
    def retrieve(self, request, *args, **kwargs):
        ret = {'code': 1000}
        pk = kwargs.get('pk')
        account = models.Account.objects.filter(id=pk).first()
        if not account:
            ret['code'] = 4004
            ret['error'] = '此用户不存在'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)

        try:
            ser = accountserializer.AccountAdminSerializer(instance=account, many=False)
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            ret['code'] = 2000
            ret['error'] = '获取此用户信息失败！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 修改某个用户信息
    def put(self, request, *args, **kwargs):
        """博主修改用户个人信息api"""
        ret = {'code': 1000}
        pk = kwargs.get('pk')
        account = models.Account.objects.filter(id=pk).first()
        if not account:
            ret['code'] = 4004
            ret['error'] = '此用户不存在！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        ser = accountserializer.AccountAdminSerializer(account, data=request.data, partial=True)
        if ser.is_valid():
            try:
                ser.save()
                ret['data'] = ser.data
                return Response(ret)
            except Exception as e:
                print(e)
                ret['code'] = 2000
                ret['error'] = '修改用户信息失败！'
                return Response(ret)
                # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            print(ret['error'])
            return Response(ret)
            # return Response(ret,status=status.HTTP_400_BAD_REQUEST)

    # 删除某个用户
    def delete(self, request, *args, **kwargs):
        """博主修改用户个人信息api"""
        ret = {'code': 1000}
        pk = kwargs.get('pk')
        account = models.Account.objects.filter(id=pk).first()
        if not account:
            ret['code'] = 4004
            ret['error'] = '此用户不存在！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        ser = accountserializer.AccountAdminSerializer(instance=account, many=False)
        try:
            ret['data'] = ser.data
            account.delete()
            return Response(ret)
        except Exception as e:
            ret.pop('data')
            ret['code'] = 2000
            ret['error'] = '删除用户失败'
            return Response(ret)
            # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 新增用户
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000}
        ser = accountserializer.AccountAdminSerializer(data=request.data)
        if ser.is_valid():
            try:
                ser.save()
                ret['data'] = ser.data
                return Response(ret)
            except Exception as e:
                print(e)
                ret['code'] = 2000
                ret['error'] = '用户新增失败！'
                return Response(ret)
                # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            return Response(ret)
            # return Response(ret,status=status.HTTP_400_BAD_REQUEST)





# 测试视图
class testView(APIView):
    # permission_classes = [BloggerPermission, ]
    def post(self, request, *args, **kwargs):
        print(request.FILES['img'])
        return Response({"ser": "123"})
