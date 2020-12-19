from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
from rest_framework import status
# 自定义登录认证
from api.utils.myauth import KennyAuthentication
# 博主权限
from api.utils.mypermission import BloggerPermission
from qiniu import Auth, etag,BucketManager
from api import models
import json
with open('env.json') as env:
    ENV = json.load(env)
access_key = ENV['QN_ACCESS_KEY']
secret_key = ENV['QN_SECRET_KEY']
bucket_name = ENV['QN_BUCKET_NAME']
domain=''
q = Auth(access_key, secret_key)

# 用户头像以及文章标题图内容图token获取
class ImageUploadTokenView(ViewSetMixin, APIView):
    authentication_classes = [KennyAuthentication, ]

    def userimagetoken(self, request, *args, **kwargs):
        ret = {'code': 1000}
        # key=kwargs.get('key')
        # key = str(request.user) + 'image'
        policy={
            "returnBody":  '{"key": $(key), "hash": $(etag), "url":"http://qn.kennyeow.com/$(etag)","code":1000}'
        }
        # 过期时间一天
        try:
            token = q.upload_token(bucket_name,None, 86400,policy)
            ret['data'] = token
            return Response(ret)
        except Exception as e:
            ret['code'] = 2000
            ret['error'] = "获取图片上传token失败！"
            return Response(ret)
            # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#博主上传图片token获取
class BloggerImageUploadTokenView(APIView):
    authentication_classes = [KennyAuthentication,]
    permission_classes = [BloggerPermission,]

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000}
        # key = str(request.user) + 'galleryphoto'
        policy = {
            "returnBody": '{"key": $(key), "hash": $(etag), "url":"http://qn.kennyeow.com/$(etag)","code":1000}'
        }
        # 过期时间一周
        try:
            token = q.upload_token(bucket_name, None, 604800,policy)
            ret['data'] = token
            return Response(ret)
        except Exception as e:
            ret['code'] = 2000
            ret['error'] = "获取博主图片上传token失败！"
            return Response(ret)
            # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 根据url上传七牛云，返回url
class UploadUrlToQiniuView(APIView):
    def post(self,request,*args,**kwargs):
        ret={'code':1000}
        url=request.data['url']
        if not url:
            ret['code']=4002
            ret['error']='未传递图片url'
            return Response(ret)
            # return Response(ret,status=status.HTTP_400_BAD_REQUEST)
        bucket = BucketManager(q)
        key=url.split('/')[-1]
        try:
            ret1, info = bucket.fetch(url, bucket_name, key)
            ret['data']='qn.kennyeow.com/'+ret1['key']
            return Response(ret)
        except Exception as e:
            ret.pop('data')
            ret['code']=2000
            ret['error']='上传图片失败'
            return Response(ret)
            # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 根据key值删除空间中的文件
class DeleteImageFromQiniuView(APIView):
    def delete(self,request,*args,**kwargs):
        ret = {'code': 1000}
        key = kwargs.get('key')
        # 初始化BucketManager
        bucket = BucketManager(q)
        # 删除bucket_name 中的文件 key
        ret1, info = bucket.delete(bucket_name, key)
        print(ret1)
        if ret1=={}:
            ret['code']=1000
        else:
            ret['code']=2000
            ret['error']='七牛云图片删除失败'
        return Response(ret)