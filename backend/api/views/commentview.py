# 引入models模型类
from api import models
from api.serializers import articleserializer,likeserializer,commentserializer
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
# 引入自定义分页类
from api.utils.mypagination import MyPageNumberPagination
# 引入状态码
from rest_framework import status


# 文章评论获取
class ArticleCommentReadView(APIView):
    # 不登录也可，但是登录能获取列表中的评论是否被当前用户点赞
    authentication_classes = [KennyAuthenticationForUser,]
    def get(self,request,*args,**kwargs):
        ret={'code':1000}
        pk=kwargs.get('pk')
        if not pk:
            ret['code']=4002
            ret['error']='未传递文章id值'
            return Response(ret)
            # return Response(ret,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        article=models.Article.objects.filter(id=pk).first()
        if not article:
            ret['code']=4004
            ret['error']='此文章不存在'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        comments=article.comment_list.filter(parent=None).order_by('-created')
        if not comments:
            ret['code']=1001
            ret['error']='此文章暂无评论'
            return Response(ret)
        try:
            if request.user:
                ser=commentserializer.CommentReadListSerializer(instance=comments,many=True,context={'curuser':request.user})
            else:
                ser=commentserializer.CommentReadListSerializer(instance=comments,many=True)
            ret['data']=ser.data
            return Response(ret)
        except Exception as e:
            print(e)
            ret['code']=2000
            ret['error']='获取评论失败'
            return Response(ret)
            # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 获得某条id的评论
class CommentDetailReadView(APIView):
    authentication_classes = [KennyAuthenticationForUser, ]
    def get(self, request, *args, **kwargs):
        ret = {'code': 1000}
        pk = kwargs.get('pk')
        if not pk:
            ret['code']=4002
            ret['error']='未传递评论id值'
            return Response(ret)

        comment=models.Comment.objects.filter(id=pk).first()
        if not comment:
            ret['code'] = 4004
            ret['error'] = '无此评论'
            return Response(ret)
        try:
            if request.user:
                ser = commentserializer.CommentReadDetailSerializer(instance=comment, many=False,
                                                                  context={'curuser': request.user})
            else:
                ser = commentserializer.CommentReadDetailSerializer(instance=comment, many=False)
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            print(e)
            ret['code'] = 2000
            ret['error'] = '获取评论失败'
            return Response(ret)


# 由于增加评论和删除评论所需要传递的参数不同，因此分为两个视图
class ArticleCommentAddView(APIView):
    """文章评论视图，需要登录"""
    authentication_classes = [KennyAuthentication,]
    # 发表评论
    def post(self,request,*args,**kwargs):
        ret={'code':1000}
        # 文章id值，不能为空
        article_pk=kwargs.get('article_pk')
        # 父评论id值，可以为空
        comment_pk=kwargs.get('comment_pk')
        if not article_pk:
            ret['code']='4002'
            ret['error']='未传递文章id值'
            return Response(ret)
            # return Response(ret,status=status.HTTP_400_BAD_REQUEST)
        article=models.Article.objects.filter(id=article_pk).first()
        if not article:
            ret['code']=4004
            ret['error']='此文章不存在'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        # 处理增加父评论，即文章的第一级评论
        if not comment_pk:
            ser=commentserializer.CommentManipulateSerializer(data=request.data)
            if ser.is_valid():
                try:
                    ser.save(user=request.user,parent=None,reply_to=None,content_object=article)
                    # 新增评论详情序列化，用以返回
                    newcomment = models.Comment.objects.filter(id=ser.data['id']).first()
                    ser1 = commentserializer.CommentReadDetailSerializer(instance=newcomment, many=False)
                    ret['data']=ser1.data
                    return Response(ret)
                except Exception as e:
                    print(e)
                    ret['code']='2000'
                    ret['error']='评论失败'
                    return Response(ret)
                    # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # 处理增加子评论，需要comment_pk,同时将评论等级设置为两级，超过两级的通过reply_to确定评论的评论人与被评论人
        else:
            # 获取父评论
            parent_comment=models.Comment.objects.filter(id=comment_pk).first()
            if not parent_comment:
                ret['code']=4004
                ret['error']='此父评论不存在'
                return Response(ret)
                # return Response(ret,status=status.HTTP_404_NOT_FOUND)
            # 如果该父评论存在父评论，则将父评论重置为父评论的父评论(根评论的父评论是其本身)
            parent=parent_comment.get_root()
            ser = commentserializer.CommentManipulateSerializer(data=request.data)
            if ser.is_valid():
                try:
                    # 将reply_to设置为真实父评论的user
                    ser.save(user=request.user, parent=parent, reply_to=parent_comment.user, content_object=article)
                    # 新增评论详情序列化，用以返回
                    newcomment = models.Comment.objects.filter(id=ser.data['id']).first()
                    ser1 = commentserializer.CommentReadDetailSerializer(instance=newcomment, many=False)
                    ret['data'] = ser1.data
                    return Response(ret)
                except Exception as e:
                    print(e)
                    ret['code'] = '2000'
                    ret['error'] = '评论失败'
                    return Response(ret)
                    # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(ret)


class ArticleCommentDeleteView(APIView):
    """文章评论删除视图，需要登录"""
    authentication_classes = [KennyAuthentication, ]
    # 删除评论（评论者、文章作者、博主可以删除）
    def delete(self, request, *args, **kwargs):
        ret = {'code': 1000}
        pk = kwargs.get('pk')
        if not pk:
            ret['code'] = 4002
            ret['error'] = '未传递评论id值'
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        comment = models.Comment.objects.filter(id=pk).first()
        if not comment:
            ret['code'] = 4004
            ret['error'] = '评论不存在'
            return Response(ret)
            # return Response(ret, status=status.HTTP_404_NOT_FOUND)
        # 获取评论的文章作者
        article_author = comment.content_object.author
        # 评论者、文章作者、博主可以删除评论
        if request.user == comment.user or request.user.role == 3 or request.user == article_author:
            try:
                ser = commentserializer.CommentReadDetailSerializer(instance=comment, many=False)
                ret['data'] = ser.data
                comment.delete()
                return Response(ret)
            except Exception as e:
                ret.pop('data')
                ret['code'] = 2000
                ret['error'] = '评论删除失败'
                return Response(ret)
                # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4006
            ret['error'] = '您的权限不足，无法删除评论！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_403_FORBIDDEN)







