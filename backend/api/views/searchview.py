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
# 引入ContentType表，用于获取某个人的文章点赞对象（因为也有可能是）
from django.contrib.contenttypes.models import ContentType
# 引入自定义分页类
from api.utils.mypagination import MyPageNumberPagination
# 引入状态码
from rest_framework import status
# 用于 filter id__in 按列表顺序显示
from django.db.models import Case, When, Count

from drf_haystack.viewsets import HaystackViewSet, HaystackGenericAPIView
from api.serializers.searchserializer import ArticleForSearchSerializer
from rest_framework.mixins import ListModelMixin

# 搜索视图，无需登录
class ArticleSearchView(HaystackGenericAPIView):
    # 需要获取当前用户来判定是否点赞和收藏
    authentication_classes = [KennyAuthenticationForUser, ]
    index_models = [models.Article]
    serializer_class = ArticleForSearchSerializer

    def get(self, request, *args, **kwargs):
        ret = {'code':1000}
        article_queryset=self.get_queryset()
        search_articles = self.filter_queryset(article_queryset)
        if not search_articles:
            ret['code']=1001
            ret['error']='未搜索到相关文章'
            return Response(ret)
        sort_param = request.query_params.get('sort')
        if sort_param == 'newest':
            search_articles = search_articles.order_by('-created')
        elif sort_param == 'popular':
            search_articles = search_articles.order_by('-article_likes')
        else:
            search_articles = search_articles.order_by('created')
        try:
            # 加入分页
            pg = MyPageNumberPagination()
            try:
                pager_articles = pg.paginate_queryset(queryset=search_articles, request=request, view=self)
            except Exception as e:
                ret['code'] = 1002
                ret['error'] = '暂无更多文章！'
                return Response(ret)
            ser = ArticleForSearchSerializer(instance=pager_articles, many=True, context={'request': request,'curuser':request.user})
            ret['data']=ser.data
            return Response(ret)
        except Exception as e:
            ret['code']=2000
            ret['error']='搜索文章失败'
            return Response(ret)
            # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
