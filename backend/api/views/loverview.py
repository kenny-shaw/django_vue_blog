# 引入models模型类
from api import models
from api.serializers import articleserializer, likeserializer, favoriteserializer,loverserializer
# 引入APIView、ViewSetMixin视图类，以及Response，无需进行json的序列化
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
# 自定义登录认证
from api.utils.myauth import KennyAuthentication,KennyAuthenticationForUser
# 博主权限
from api.utils.mypermission import BloggerPermission
# 引入f函数
from django.db.models import F
# 计算指定对象的个数
from django.db.models import Count
# 引入ContentType表
from django.contrib.contenttypes.models import ContentType
# 引入Q对象，多字段查询
from django.db.models import Q
# 引入自定义分页类
from api.utils.mypagination import MyPageNumberPagination
# 引入状态码
from rest_framework import status
# 用于 filter id__in 按列表顺序显示
from django.db.models import Case, When


# 情侣查看api
class LoverReadView(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 1000}
        lover = models.Lovers.objects.first()
        if not lover:
            ret['code'] = 4004
            ret['error'] = '此情侣不存在'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        ser = loverserializer.LoverSerializer(instance=lover, many=False)
        ret['data'] = ser.data
        return Response(ret)

class LoverManipulateView(APIView):
    # 需要登录认证
    authentication_classes = [KennyAuthentication, ]
    # 权限等级为博主，只有博主才可进行操作
    permission_classes = [BloggerPermission, ]
    def put(self,request,*args,**kwargs):
        ret = {'code': 1000}
        lover = models.Lovers.objects.first()
        if not lover:
            ret['code'] = 4004
            ret['error'] = '此情侣不存在'
            return Response(ret)
            # return Response(ret, status=status.HTTP_404_NOT_FOUND)
        ser = loverserializer.LoverSerializer(lover, data=request.data, partial=True)
        if ser.is_valid():
            try:
                ser.save()
                ret['data'] = ser.data
                return Response(ret)
            except Exception as e:
                print(e)
                ret['code'] = 2000
                ret['error'] = '修改情侣信息失败'
                return Response(ret)
                # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)