# 引入models模型类
from api import models
from api.serializers import articleserializer, likeserializer
# 引入APIView、ViewSetMixin视图类，以及Response，无需进行json的序列化
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
# 自定义登录认证
from api.utils.myauth import KennyAuthentication,KennyAuthenticationForUser
# 博主权限
from api.utils.mypermission import BloggerPermission
# 引入ContentType表，用于获取某个人的文章点赞对象（因为也有可能是评论）
from django.contrib.contenttypes.models import ContentType
# 引入自定义分页类
from api.utils.mypagination import MyPageNumberPagination
# 引入状态码
from rest_framework import status
# 用于 filter id__in 按列表顺序显示
from django.db.models import Case, When


# 文章点赞查看api，用于查询用户点赞的文章
class ArticleLikeReadView(APIView):
    # 此认证，只辨别当前用户，来获取是否对各个文章点赞收藏等
    authentication_classes = [KennyAuthenticationForUser,]
    # 查看用户点赞的文章列表api（无需登陆认证）, 需要传入pk
    def get(self, request, *args, **kwargs):
        ret = {'code': 1000}
        pk = kwargs.get('pk')
        if not pk:
            ret['code'] = 4002
            ret['error'] = '未传递用户id'
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        user = models.Account.objects.filter(id=pk).first()
        if not user:
            ret['code'] = 4004
            ret['error'] = '此用户不存在'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        # 获取文章表
        articletable = ContentType.objects.filter(model='article').first()
        # 获取表为文章表，且是该用户喜欢的文章对象
        like_objs = models.Like.objects.filter(user=user, content_type=articletable)
        # 用户没有喜欢的文章
        if not like_objs:
            ret['code'] = 1001
            ret['error'] = '此用户暂无喜欢的文章~'
            return Response(ret)
        # 通过喜欢对象(即文章对象)记录其id组成数组
        like_araticleids = [item.content_object.id for item in like_objs]
        # 按照like_araticleids中的顺序展示
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(like_araticleids)])
        # 查询id在数组内的文章对象
        like_articles = models.Article.objects.filter(id__in=like_araticleids).order_by(preserved)
        sort_param = request.query_params.get('sort')
        if sort_param == 'newest':
            like_articles = like_articles.order_by('-created')
        elif sort_param == 'popular':
            like_articles = like_articles.order_by('-total_views')
        # 防止不order_by时分页警告
        else:
            like_articles = like_articles.order_by('created')
        print(like_articles.first().id)
        try:
            # 加入分页
            pg = MyPageNumberPagination()
            try:
                pager_like_articles = pg.paginate_queryset(queryset=like_articles, request=request, view=self)
            except Exception as e:
                ret['code'] = 1002
                ret['error'] = '暂无更多喜欢的文章！'
                return Response(ret)
            ser = articleserializer.ArticleReadListSerializer(instance=pager_like_articles, many=True,context={'curuser': request.user})
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            ret['code'] = 2000
            ret['error'] = '获取该用户喜欢的文章失败！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 文章点赞操作api，主要用于用户对文章进行点赞，以及取消点赞
class ArticleLikeManipulateView(APIView):
    # 需要登录才可进行点赞，取消点赞
    authentication_classes = [KennyAuthentication, ]

    # 增加点赞，用户对文章点赞
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000}
        pk = kwargs.get('pk')
        if not pk:
            ret['code'] = 4002
            ret['error'] = '未传递文章id'
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        article = models.Article.objects.filter(id=pk).first()
        if not article:
            ret['code'] = 4004
            ret['error'] = '此文章不存在或已被删除！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)

        # 查找点赞表，看是否已点赞，如果已点赞，不能继续点赞
        likeobj = article.like_list.filter(user=request.user).first()
        if likeobj:
            ret['code'] = 4003
            ret['error'] = '您已经点赞了哟'
            return Response(ret)
            # return Response(ret, status=status.HTTP_403_FORBIDDEN)
        ser = likeserializer.LikeSerializer(data=request.data)
        if ser.is_valid():
            try:
                ser.save(user=request.user, content_object=article)
                ret['data'] = ser.data
                return Response(ret)
            except Exception as e:
                ret['code'] = 2000
                ret['error'] = '点赞失败！'
                return Response(ret)
                # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    # 删除点赞
    def delete(self, request, *args, **kwargs):
        ret = {'code': 1000}
        pk = kwargs.get('pk')
        if not pk:
            ret['code'] = 4002
            ret['error'] = '未传递文章id值'
            return Response(ret)
            # return Response(ret, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        article = models.Article.objects.filter(id=pk).first()
        if not article:
            ret['code'] = 4004
            ret['error'] = '此文章不存在或已被删除！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        # 查找点赞表，看是否已点赞，如果已点赞，不能继续点赞
        likeobj = article.like_list.filter(user=request.user).first()
        if not likeobj:
            ret['code'] = 4003
            ret['error'] = '您尚未点赞哦~'
            return Response(ret)
            # return Response(ret, status=status.HTTP_403_FORBIDDEN)
        try:
            ser = likeserializer.LikeSerializer(instance=likeobj, many=False)
            ret['data'] = ser.data
            likeobj.delete()
            return Response(ret)
        except Exception as e:
            ret.pop('data')
            ret['code'] = 2000
            ret['error'] = '取消点赞失败！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 评论点赞操作api
class CommentLikeManipulateView(APIView):
    # 需要登录认证
    authentication_classes = [KennyAuthentication,]
    # 点赞评论
    def post(self,request,*args,**kwargs):
        ret={'code':1000}
        # 获取评论的id
        pk=kwargs.get('pk')
        if not pk:
            ret['code']=4002
            ret['error']='未传递评论id值'
            return Response(ret)
            # return Response(ret,status=status.HTTP_400_BAD_REQUEST)
        comment=models.Comment.objects.filter(id=pk).first()
        if not comment:
            ret['code']=4004
            ret['error']='评论不存在'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        # 查找点赞表，看是否已点赞，如果已点赞，不能继续点赞
        likeobj = comment.like_list.filter(user=request.user).first()
        if likeobj:
            ret['code'] = 4003
            ret['error'] = '您已经点赞了哟'
            return Response(ret)
            # return Response(ret, status=status.HTTP_403_FORBIDDEN)
        ser = likeserializer.LikeSerializer(data=request.data)
        if ser.is_valid():
            try:
                ser.save(user=request.user, content_object=comment)
                ret['data'] = ser.data
                return Response(ret)
            except Exception as e:
                ret['code'] = 2000
                ret['error'] = '点赞失败！'
                return Response(ret)
                # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    # 删除点赞
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
            ret['error'] = '此评论不存在或已被删除！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        # 查找点赞表，看是否已点赞，如果已点赞，不能继续点赞
        likeobj = comment.like_list.filter(user=request.user).first()
        if not likeobj:
            ret['code'] = 4003
            ret['error'] = '您尚未点赞哦~'
            return Response(ret)
            # return Response(ret, status=status.HTTP_403_FORBIDDEN)
        try:
            ser = likeserializer.LikeSerializer(instance=likeobj, many=False)
            ret['data'] = ser.data
            likeobj.delete()
            return Response(ret)
        except Exception as e:
            ret.pop('data')
            ret['code'] = 2000
            ret['error'] = '取消点赞失败！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
