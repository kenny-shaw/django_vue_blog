# 引入models模型类
from api import models
from api.serializers import articleserializer, likeserializer, favoriteserializer
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

# 收藏夹列表获取
class FavoriteReadListView(APIView):
    """收藏夹列表获取"""

    # 获取收藏夹列表，需要用户pk参数,另外当前文章id可传递也可不传递，以便从文章页面查看是否被收藏夹列表中的收藏夹收藏
    def get(self, request, *args, **kwargs):
        ret = {'code': 1000}
        user_pk = kwargs.get('user_pk')
        if not user_pk:
            ret['code'] = 4002
            ret['error'] = '未传递用户id'
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        user = models.Account.objects.filter(id=user_pk).first()
        if not user:
            ret['code'] = 4004
            ret['error'] = '用户不存在'
            return Response(ret)
            # return Response(ret, status=status.HTTP_404_NOT_FOUND)
        favorites = models.Favorite.objects.filter(user=user).order_by('-createdorupdated')
        if not favorites:
            ret['code'] = 1001
            ret['error'] = '此用户暂无收藏夹'
            return Response(ret)
        # 加入分页
        pg = MyPageNumberPagination()
        try:
            pager_favorites = pg.paginate_queryset(queryset=favorites, request=request, view=self)
        except Exception as e:
            ret['code'] = 1002
            ret['error'] = '暂无更多收藏夹！'
            return Response(ret)

        try:
            article=''
            article_pk = kwargs.get('article_pk')
            if article_pk:
                article = models.Article.objects.filter(id=article_pk).first()
                if not article:
                    ret['code'] = 4004
                    ret['error'] = '当前文章不存在'
                    return Response(ret)
                    # return Response(ret,status=status.HTTP_404_NOT_FOUND)
            if article:
                ser = favoriteserializer.FavoriteReadSerializer(instance=pager_favorites, many=True,context={'curarticle':article})
            else:
                ser = favoriteserializer.FavoriteReadSerializer(instance=pager_favorites, many=True)
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            print(e)
            ret['code'] = 2000
            ret['error'] = '获取收藏夹列表失败'
            return Response(ret)
            # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 由于和收藏夹列表获取都需要一个参数，所以新建一个视图用来获取收藏夹详情
class FavoriteReadDetailView(APIView):
    # 获取某个收藏夹列表详情，需要传递收藏夹id,与获取文章分开，避免更改收藏夹信息时，再次加载所有文章
    def get(self, request, *args, **kwargs):
        ret = {'code': 1000}
        pk = kwargs.get('pk')
        if not pk:
            ret['code'] = 4002
            ret['error'] = '未传递收藏夹id！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        # 收藏夹详情中文章的排序规则参数，分为newest与popular
        # sort_param = request.query_params.get('sort')
        favorite = models.Favorite.objects.filter(id=pk).first()
        if not favorite:
            ret['code'] = 4004
            ret['error'] = '此收藏夹不存在！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_404_NOT_FOUND)
        try:
            # if sort_param == 'newest':
            #     favorite.article.set(favorite.article.order_by('-created'))
            # elif sort_param == 'popular':
            #     favorite.article.set(favorite.article.order_by('-total_views'))
            # else:
            #     favorite.article.set(favorite.article.order_by('created'))
            ser = favoriteserializer.FavoriteReadSerializer(instance=favorite, many=False)
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            print(e)
            ret['code'] = 2000
            ret['error'] = '获取收藏夹详情失败！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 获取收藏夹的所有文章列表
class FavoriteArticleListView(APIView):
    # 此认证，只辨别当前用户，来获取是否对各个文章点赞收藏等
    authentication_classes = [KennyAuthenticationForUser, ]
    def get(self, request, *args, **kwargs):
        ret = {'code': 1000}
        pk = kwargs.get('pk')
        if not pk:
            ret['code'] = 4002
            ret['error'] = '未传递收藏夹id'
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        # 收藏夹详情中文章的排序规则参数，分为newest与popular
        sort_param = request.query_params.get('sort')
        favorite = models.Favorite.objects.filter(id=pk).first()
        if not favorite:
            ret['code'] = 4004
            ret['error'] = '此收藏夹不存在'
            return Response(ret)
            # return Response(ret, status=status.HTTP_404_NOT_FOUND)
        articles = favorite.article.all().order_by('-link_to_favorite')
        if not articles:
            ret['code'] = 1001
            ret['error'] = '此收藏夹暂无文章！'
            return Response(ret)
        # if sort_param == 'newest':
        #     articles = articles.order_by('-created')
        # elif sort_param == 'popular':
        #     articles = articles.order_by('-total_views')
        # else:
        #     articles = articles.order_by('created')
        try:
            # 加入分页
            pg = MyPageNumberPagination()
            try:
                pager_articles = pg.paginate_queryset(queryset=articles, request=request, view=self)
            except Exception as e:
                print(e)
                ret['code'] = 1002
                ret['error'] = '暂无更多文章！'
                return Response(ret)
            ser = articleserializer.ArticleReadListSerializer(instance=pager_articles, many=True, context={'curuser': request.user})
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            print(e)
            ret['code'] = 2000
            ret['error'] = '获取收藏夹文章列表失败'
            return Response(ret)
            # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 增加、修改、删除收藏夹信息视图（只包括标题和简介，不包括文章，收藏与取消收藏文章，专门使用一个视图）
class FavoriteManipulateView(APIView):
    # 需要登录认证
    authentication_classes = [KennyAuthentication, ]
    # 增加收藏夹
    def post(self,request,*args,**kwargs):
        ret={'code':1000}
        # pk只用于put与delete
        pk = kwargs.get('pk')
        if pk:
            ret['code'] = 4005
            ret['error'] = '此api不存在'
            return Response(ret)
            # return Response(ret, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        ser=favoriteserializer.FavoriteManipulateSerializer(data=request.data)
        if ser.is_valid():
            try:
                ser.save(user=request.user)
                # 以Read序列化再次返回
                newfavorite= models.Favorite.objects.filter(id=ser.data['id']).first()
                ser1 = favoriteserializer.FavoriteReadSerializer(instance=newfavorite, many=False)
                ret['data'] = ser1.data
                return Response(ret)
            except Exception as e:
                print(e)
                ret['code']=2000
                ret['error']="新建收藏夹失败"
                return Response(ret)
                # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code']=4001
            ret['error']=ser.errors
            return Response(ret)
            # return Response(ret,status=status.HTTP_400_BAD_REQUEST)
    # 修改收藏夹
    def put(self, request, *args, **kwargs):
        ret = {'code': 1000}
        # 获取收藏夹id
        pk = kwargs.get('pk')
        if not pk:
            ret['code'] = 4002
            ret['error'] = '未传递收藏夹id'
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        favorite = models.Favorite.objects.filter(id=pk).first()
        if not favorite:
            ret['code'] = 4004
            ret['error'] = '收藏夹不存在'
            return Response(ret)
            # return Response(ret, status=status.HTTP_404_NOT_FOUND)
        if favorite.user != request.user:
            ret['code'] = 4006
            ret['error'] = '您无法修改他人的收藏夹'
            return Response(ret)
            # return Response(ret, status=status.HTTP_403_FORBIDDEN)
        ser = favoriteserializer.FavoriteManipulateSerializer(favorite, data=request.data,partial=True)
        if ser.is_valid():
            try:
                ser.save()
                # 以Read序列化再次返回
                newfavorite = models.Favorite.objects.filter(id=ser.data['id']).first()
                ser1 = favoriteserializer.FavoriteReadSerializer(instance=newfavorite, many=False)
                ret['data'] = ser1.data
                return Response(ret)
            except Exception as e:
                ret['code'] = 2000
                ret['error'] = '修改收藏夹信息失败'
                return Response(ret)
                # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    # 删除收藏夹
    def delete(self, request, *args, **kwargs):
        ret = {'code': 1000}
        # 获取收藏夹id
        pk = kwargs.get('pk')
        if not pk:
            ret['code'] = 4002
            ret['error'] = '未传递收藏夹id'
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        favorite = models.Favorite.objects.filter(id=pk).first()
        if not favorite:
            ret['code'] = 4004
            ret['error'] = '收藏夹不存在'
            return Response(ret)
            # return Response(ret, status=status.HTTP_404_NOT_FOUND)
        if favorite.user != request.user:
            ret['code'] = 4006
            ret['error'] = '您无法删除他人的收藏夹'
            return Response(ret)
            # return Response(ret, status=status.HTTP_403_FORBIDDEN)
        try:
            ser = favoriteserializer.FavoriteReadSerializer(instance=favorite,many=False)
            ret['data'] = ser.data
            favorite.delete()
            return Response(ret)
        except Exception as e:
            ret.pop('data')
            ret['code'] = 2000
            ret['error'] = '删除收藏夹信息失败'
            return Response(ret)
            # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# 用户收藏文章到收藏夹以及某收藏夹取消收藏某文章视图
class FavoriteArticleManipulateView(APIView):
    # 需要登录
    authentication_classes = [KennyAuthentication, ]

    # 收藏文章到收藏夹，需要传递收藏夹id，文章id
    def post(self,request,*args,**kwargs):
        ret={'code':1000}
        favorite_pk=kwargs.get('favorite_pk')
        article_pk=kwargs.get('article_pk')
        if not favorite_pk or not article_pk:
            ret['code']=4002
            ret['error']='未传递收藏夹id或者文章id'
            return Response(ret)
            # return Response(ret,status=status.HTTP_400_BAD_REQUEST)
        favorite=models.Favorite.objects.filter(id=favorite_pk).first()
        article=models.Article.objects.filter(id=article_pk).first()
        if not favorite or not article:
            ret['code']=4004
            ret['error']='收藏夹或文章不存在'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        if favorite.user!=request.user:
            ret['code'] = 4006
            ret['error'] = '您没有权限进行此操作！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_403_FORBIDDEN)
        articleobj=favorite.article.filter(id=article.id)
        if articleobj:
            ret['code']=4003
            ret['error']='您已经将此文章添加至该收藏夹'
            return Response(ret)
            # return Response(ret,status=status.HTTP_403_FORBIDDEN)
        # 向收藏夹添加该文章
        try:
            favorite.article.add(article)
            ser=articleserializer.ArticleReadDetailSerializer(instance=article,many=False)
            ret['data']=ser.data
            return Response(ret)
        except Exception as e:
            ret['code']=2000
            ret['error']='将文章添加至收藏夹失败！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 移除某收藏夹的某文章
    def delete(self,request,*args,**kwargs):
        ret = {'code': 1000}
        favorite_pk = kwargs.get('favorite_pk')
        article_pk = kwargs.get('article_pk')
        if not favorite_pk or not article_pk:
            ret['code'] = 4002
            ret['error'] = '未传递收藏夹id或者文章id'
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        favorite = models.Favorite.objects.filter(id=favorite_pk).first()
        article = models.Article.objects.filter(id=article_pk).first()
        if not favorite or not article:
            ret['code'] = 4004
            ret['error'] = '收藏夹或文章不存在'
            return Response(ret)
            # return Response(ret, status=status.HTTP_404_NOT_FOUND)
        if favorite.user != request.user:
            ret['code'] = 4006
            ret['error'] = '您没有权限进行此操作！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_403_FORBIDDEN)
        articleobj = favorite.article.filter(id=article.id)
        if not articleobj:
            ret['code'] = 4003
            ret['error'] = '此文章不在该收藏夹中'
            return Response(ret)
            # return Response(ret, status=status.HTTP_403_FORBIDDEN)
        # 收藏夹移除该文章
        try:
            favorite.article.remove(article)
            ser = articleserializer.ArticleReadDetailSerializer(instance=article, many=False)
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            print(e)
            ret['code'] = 2000
            ret['error'] = '收藏夹移除该文章失败！'
            return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
