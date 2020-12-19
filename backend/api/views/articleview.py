# 引入models模型类
from api import models
from api.serializers import articleserializer, likeserializer
# 引入APIView、ViewSetMixin视图类，以及Response，无需进行json的序列化
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
# 自定义登录认证
from api.utils.myauth import KennyAuthentication, KennyAuthenticationForUser
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
from bs4 import BeautifulSoup

# html转text
def Html2Text(html):
    soup = BeautifulSoup(html,features='html.parser')

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


# 获取文章列表，以及某文章详细信息视图（无需登录认证）
class ArticleReadView(ViewSetMixin, APIView):
    # 此认证，只辨别当前用户，来获取是否对各个文章点赞收藏等
    authentication_classes = [KennyAuthenticationForUser, ]

    # 获取文章列表
    def list(self, request, *args, **kwargs):
        ret = {'code': 1000}
        articles = models.Article.objects.all()
        # 获取属于某个column或者tag的文章列表
        column_param = request.query_params.get('column')
        tag_param = request.query_params.get('tag')
        sort_param = request.query_params.get('sort')
        if column_param:
            column_obj = models.ArticleColumn.objects.filter(title=column_param).first()
            articles = models.Article.objects.filter(column=column_obj)
        if tag_param:
            tag_obj = models.ArticleTag.objects.filter(title=tag_param).first()
            articles = models.Article.objects.filter(tag=tag_obj)
        if sort_param == 'newest':
            articles = articles.order_by('-created')
        elif sort_param == 'popular':
            articles = articles.order_by('-total_views')
        # 防止不order_by时分页警告
        else:
            articles = articles.order_by('created')

        if not articles:
            ret['code'] = 1001
            ret['error'] = '暂无文章~'
            return Response(ret)
        try:
            # 加入分页
            pg = MyPageNumberPagination()
            try:
                pager_articles = pg.paginate_queryset(queryset=articles, request=request, view=self)
            except Exception as e:
                ret['code'] = 1002
                ret['error'] = '暂无更多文章！'
                return Response(ret)
            # 如果存在当前用户，则将当前用户传递过去，用以获取当前文章是否被当前用户点赞
            if request.user:
                ser = articleserializer.ArticleReadListSerializer(instance=pager_articles, many=True,
                                                                  context={'curuser': request.user})
            else:
                ser = articleserializer.ArticleReadListSerializer(instance=pager_articles, many=True)
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            ret['code'] = 2000
            ret['error'] = '获取文章列表失败！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 获取id为pk的文章详情
    def retrieve(self, request, *args, **kwargs):
        ret = {'code': 1000}
        pk = kwargs.get('pk')
        article = models.Article.objects.filter(id=pk).first()
        if not article:
            ret['code'] = 4004
            ret['error'] = '文章不存在~'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        try:
            # 访问一次增加一次浏览量,F函数直接操作数据库，减少内存消耗
            article.total_views = F('total_views') + 1
            article.save()
            # 正因为 F 函数没有在内存中操作，因此更新完数据后需要重新刷新内存中的模型对象
            article.refresh_from_db()
            if request.user:
                ser = articleserializer.ArticleReadDetailSerializer(instance=article, many=False,
                                                                    context={'curuser': request.user})
            else:
                ser = articleserializer.ArticleReadDetailSerializer(instance=article, many=False)
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            print(e)
            ret['code'] = 2000
            ret['error'] = '获取文章详情失败！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 获取某用户的文章
class UserArticleReadView(APIView):
    # 此认证，只辨别当前用户，来获取是否对各个文章点赞收藏等
    authentication_classes = [KennyAuthenticationForUser, ]

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000}
        # 获取作者id
        pk = kwargs.get('pk')
        author = models.Account.objects.filter(id=pk).first()
        if not author:
            ret['code'] = 4004
            ret['error'] = '该用户不存在~'
            return Response(ret)
        articles = models.Article.objects.filter(author=author)
        sort_param = request.query_params.get('sort')
        if sort_param == 'newest':
            articles = articles.order_by('-created')
        elif sort_param == 'popular':
            articles = articles.order_by('-total_views')
        # 防止不order_by时分页警告
        else:
            articles = articles.order_by('created')
        if not articles:
            ret['code'] = 1001
            ret['error'] = '该用户暂无文章~'
            return Response(ret)
        try:
            # 加入分页
            pg = MyPageNumberPagination()
            try:
                pager_articles = pg.paginate_queryset(queryset=articles, request=request, view=self)
            except Exception as e:
                ret['code'] = 1002
                ret['error'] = '暂无更多文章！'
                return Response(ret)
            # 如果存在当前用户，则将当前用户传递过去，用以获取当前文章是否被当前用户点赞
            if request.user:
                ser = articleserializer.ArticleReadListSerializer(instance=pager_articles, many=True,
                                                                  context={'curuser': request.user})
            else:
                ser = articleserializer.ArticleReadListSerializer(instance=pager_articles, many=True)
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            print(e)
            ret['code'] = 2000
            ret['error'] = '获取该用户文章列表失败！'
            return Response(ret)


# 新增文章，删除文章，更新文章内容视图（需要登录认证）
class ArticleManipulateView(APIView):
    authentication_classes = [KennyAuthentication, ]

    # 新增文章
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000}
        # pk只用于put与delete
        pk = kwargs.get('pk')
        if pk:
            ret['code'] = 4005
            ret['error'] = '此api不存在'
            return Response(ret)
            # return Response(ret,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # 看传过来的数据里是否有column，并且长度不为0
        column = None
        if 'column' in request.data and len(request.data['column']) != 0:
            column_title = request.data.pop('column')
            column = models.ArticleColumn.objects.filter(title=column_title).first()
        # 看传过来的数据里是否有column，并且该数组长度不为0
        tag = None
        if 'tag' in request.data and len(request.data['tag']) != 0:
            tag_array = request.data.pop('tag')
            # 遍历tag的title数组，看有没有该标签对象，没有的话新建标签对象
            for tag_title in tag_array:
                tagobj = models.ArticleTag.objects.filter(title=tag_title).first()
                if not tagobj:
                    data = {'title': tag_title}
                    sertag = articleserializer.ArticleTagSerializer(data=data)
                    if sertag.is_valid():
                        try:
                            sertag.save()
                        except Exception as e:
                            ret['code'] = 2000
                            ret['error'] = '添加标签失败!'
                            return Response(ret)
                            # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        ret['code'] = 4001
                        ret['error'] = sertag.errors
                        return Response(ret)
                        # return Response(ret, status=status.HTTP_400_BAD_REQUEST)
            # 获取所有在title在tag_array中的tag对象
            tag = models.ArticleTag.objects.filter(title__in=tag_array)
        request.data['content_text']=Html2Text(request.data['content_html'])

        ser = articleserializer.ArticleManipulateSerializer(data=request.data)
        if ser.is_valid():
            try:
                # 判断是否传进来了column与tag进行不同的存储
                if column and tag:
                    ser.save(author=request.user, column=column, tag=tag)
                elif column and not tag:
                    ser.save(author=request.user, column=column)
                elif tag and not column:
                    ser.save(author=request.user, tag=tag)
                else:
                    ser.save(author=request.user)
                # 以Read序列化再次返回
                newarticle = models.Article.objects.filter(id=ser.data['id']).first()
                ser1 = articleserializer.ArticleReadDetailSerializer(instance=newarticle, many=False)
                ret['data'] = ser1.data
                return Response(ret)
            except Exception as e:
                print(e)
                ret['code'] = 2000
                ret['error'] = '新增文章失败'
                return Response(ret)
                # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    # 修改id为pk的文章（不能修改他人文章，博主除外）
    def put(self, request, *args, **kwargs):
        ret = {'code': 1000}
        pk = kwargs.get('pk')
        # pk只用于put与delete
        if not pk:
            ret['code'] = 4005
            ret['error'] = '此api不存在'
            return Response(ret)
            # return Response(ret,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        article = models.Article.objects.filter(id=pk).first()
        if not article:
            ret['code'] = 4004
            ret['error'] = '该文章不存在'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        # 除博主外，其他人都不能修改别人的文章
        if article.author != request.user and request.user.role != 3:
            ret['code'] = 4006
            ret['error'] = '您无权修改他人文章'
            return Response(ret)
            # return Response(ret,status=status.HTTP_403_FORBIDDEN)

        # 看传过来的数据里是否有column，并且长度不为0
        column = None
        if 'column' in request.data and len(request.data['column']) != 0:
            column_title = request.data.pop('column')
            column = models.ArticleColumn.objects.filter(title=column_title).first()
        # 看传过来的数据里是否有column，并且该数组长度不为0
        tag = None
        if 'tag' in request.data and len(request.data['tag']) != 0:
            tag_array = request.data.pop('tag')
            # 遍历tag的title数组，看有没有该标签对象，没有的话新建标签对象
            for tag_title in tag_array:
                tagobj = models.ArticleTag.objects.filter(title=tag_title).first()
                if not tagobj:
                    data = {'title': tag_title}
                    sertag = articleserializer.ArticleTagSerializer(data=data)
                    if sertag.is_valid():
                        try:
                            sertag.save()
                        except Exception as e:
                            ret['code'] = 2000
                            ret['error'] = '添加标签失败!'
                            return Response(ret)
                            # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        ret['code'] = 4001
                        ret['error'] = sertag.errors
                        return Response(ret)
                        # return Response(ret, status=status.HTTP_400_BAD_REQUEST)
            # 获取所有在title在tag_array中的tag对象
            tag = models.ArticleTag.objects.filter(title__in=tag_array)
            request.data['content_text'] = Html2Text(request.data['content_html'])
        ser = articleserializer.ArticleManipulateSerializer(article, data=request.data)
        if ser.is_valid():
            try:
                # 判断是否传进来了column与tag进行不同的存储
                if column and tag:
                    ser.save(author=request.user, column=column, tag=tag)
                elif column and not tag:
                    ser.save(author=request.user, column=column)
                elif tag and not column:
                    ser.save(author=request.user, tag=tag)
                else:
                    ser.save(author=request.user)
                # 以Read序列化再次返回
                updatedarticle = models.Article.objects.filter(id=pk).first()
                ser1 = articleserializer.ArticleReadDetailSerializer(instance=updatedarticle, many=False)
                ret['data'] = ser1.data
                return Response(ret)
            except Exception as e:
                print(e)
                ret['code'] = 2000
                ret['error'] = '修改文章失败'
                return Response(ret)
                # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            return Response(ret)
            # return Response(ret,status=status.HTTP_400_BAD_REQUEST)

    # 删除id为pk的文章（不能修改他人文章，博主除外）
    def delete(self, request, *args, **kwargs):
        ret = {'code': 1000}
        pk = kwargs.get('pk')
        # pk只用于put与delete
        if not pk:
            ret['code'] = 4005
            ret['error'] = '此api不存在'
            return Response(ret)
            # return Response(ret,status=status.HTTP_405_METHOD_NOT_ALLOWED)

        article = models.Article.objects.filter(id=pk).first()
        if not article:
            ret['code'] = 4004
            ret['error'] = '该文章不存在或已被删除！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        # 除博主外，其他人都不能修改别人的文章
        if article.author != request.user and request.user.role != 3:
            print(request.user.role)
            ret['code'] = 4006
            ret['error'] = '您无权删除他人文章！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_403_FORBIDDEN)
        try:
            ser = articleserializer.ArticleReadDetailSerializer(instance=article, many=False)
            ret['data'] = ser.data
            article.delete()
            return Response(ret)
        except Exception as e:
            ret.pop('data')
            ret['code'] = 2000
            ret['error'] = '文章删除失败！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 获取文章栏目列表，以及栏目详情视图（不需要登录和博主权限）
class ArticleColumnReadView(ViewSetMixin, APIView):
    # 获取栏目列表
    def list(self, request, *args, **kwargs):
        ret = {'code': 1000}
        text = request.query_params.get('text')
        if text:
            columns = models.ArticleColumn.objects.filter(
                Q(title__icontains=text) | Q(brief__icontains=text)).order_by('created')
        else:
            columns = models.ArticleColumn.objects.all().order_by('created')
        ret['total'] = columns.count()
        if not columns:
            ret['code'] = 1001
            ret['error'] = '暂无文章栏目！'
            return Response(ret)
        try:
            # 加入分页
            pg = MyPageNumberPagination()
            try:
                pager_columns = pg.paginate_queryset(queryset=columns, request=request, view=self)
            except Exception as e:
                ret['code'] = 1002
                ret['error'] = '暂无更多栏目！'
                return Response(ret)
            ser = articleserializer.ArticleColumnSerializer(instance=pager_columns, many=True)
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            print(e)
            ret['code'] = 2000
            ret['error'] = '获取栏目列表失败！'
            return Response(ret)
            # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 获取栏目详情
    def retrieve(self, request, *args, **kwargs):
        ret = {'code': 1000}
        pk = kwargs.get('pk')
        column = models.ArticleColumn.objects.filter(id=pk).first()
        if not column:
            ret['code'] = 4004
            ret['error'] = '栏目不存在~'
            return Response(ret)
            # return Response(ret,status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                ser = articleserializer.ArticleColumnSerializer(instance=column, many=False)
                ret['data'] = ser.data
                return Response(ret)
            except Exception as e:
                ret['code'] = 2000
                ret['error'] = '获取栏目详情失败！'
                return Response(ret)
                # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 新增栏目，删除栏目，更新栏目详情视图（需要登录和博主权限）
class ArticleColumnManipulateView(APIView):
    # 需要登录以及博主权限
    authentication_classes = [KennyAuthentication, ]
    permission_classes = [BloggerPermission, ]

    # 增加栏目
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000}
        # pk只用于put与delete
        pk = kwargs.get('pk')
        if pk:
            ret['code'] = 4005
            ret['error'] = '此api不存在'
            return Response(ret)
            # return Response(ret,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        ser = articleserializer.ArticleColumnSerializer(data=request.data)
        if ser.is_valid():
            try:
                ser.save()
                ret['data'] = ser.data
                return Response(ret)
            except Exception as e:
                ret['code'] = 2000
                ret['error'] = '新增栏目失败！'
                return Response(ret)
                # return Response(ret,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            return Response(ret)
            # return Response(ret,status=status.HTTP_400_BAD_REQUEST)

    # 修改栏目
    def put(self, request, *args, **kwargs):
        ret = {'code': 1000}
        # pk只用于put与delete
        pk = kwargs.get('pk')
        if not pk:
            ret['code'] = 4005
            ret['error'] = '此api不存在'
            return Response(ret)
            # return Response(ret, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        column = models.ArticleColumn.objects.filter(id=pk).first()
        if not column:
            ret['code'] = 4004
            ret['error'] = '该栏目不存在或已被删除！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_404_NOT_FOUND)
        ser = articleserializer.ArticleColumnSerializer(column, data=request.data)
        if ser.is_valid():
            try:
                ser.save()
                ret['data'] = ser.data
                return Response(ret)
            except Exception as e:
                ret['code'] = 2000
                ret['error'] = '栏目修改失败！'
                return Response(ret)
                # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    # 删除栏目
    def delete(self, request, *args, **kwargs):
        ret = {'code': 1000}
        # pk只用于put与delete
        pk = kwargs.get('pk')
        if not pk:
            ret['code'] = 4005
            ret['error'] = '此api不存在'
            return Response(ret)
            # return Response(ret, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        column = models.ArticleColumn.objects.filter(id=pk).first()
        if not column:
            ret['code'] = 4004
            ret['error'] = '该栏目不存在或已被删除！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_404_NOT_FOUND)
        try:
            ser = articleserializer.ArticleColumnSerializer(instance=column, many=False)
            ret['data'] = ser.data
            column.delete()
            return Response(ret)
        except Exception as e:
            ret.pop('data')
            ret['code'] = 2000
            ret['error'] = '栏目删除失败！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 获取文章标签列表,以及标签详情（无需登录和博主权限）
class ArticleTagReadView(ViewSetMixin, APIView):
    # 查看文章标签列表
    def list(self, request, *args, **kwargs):
        ret = {'code': 1000}
        text = request.query_params.get('text')
        if text:
            tags = models.ArticleTag.objects.filter(
                Q(title__icontains=text))
        else:
            tags = models.ArticleTag.objects.all()
        sort_param = request.query_params.get('sort')
        # 去除num参数，直接借助分页可获取热度最高的前几名标签?size=10&sort=popular
        if sort_param and sort_param == 'popular':
            tags = tags.annotate(total_articles=Count('tag_article')).order_by(
                '-total_articles')
        else:
            tags = tags.order_by('created')
        if not tags:
            ret['code'] = 1001
            ret['error'] = '暂无标签哦！'
            return Response(ret)
        try:
            # 加入分页
            pg = MyPageNumberPagination()
            try:
                pager_tags = pg.paginate_queryset(queryset=tags, request=request, view=self)
            except Exception as e:
                ret['code'] = 1002
                ret['error'] = '暂无更多标签！'
                return Response(ret)
            ser = articleserializer.ArticleTagSerializer(instance=pager_tags, many=True)
            ret['data'] = ser.data
            ret['total'] = tags.count()
            return Response(ret)
        except Exception as e:
            print(e)
            ret['code'] = 2000
            ret['error'] = '获取标签列表失败！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 查看文章标签详情
    def retrieve(self, request, *args, **kwargs):
        ret = {'code': 1000}
        title = kwargs.get('title')
        print(title)
        tag = models.ArticleTag.objects.filter(title=title).first()
        if not tag:
            ret['code'] = 4004
            ret['error'] = '此标签不存在！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_404_NOT_FOUND)
        try:
            ser = articleserializer.ArticleTagSerializer(instance=tag, many=False)
            ret['data'] = ser.data
            return Response(ret)
        except Exception as e:
            print(e)
            ret['code'] = 2000
            ret['error'] = '获取标签失败！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 新增文章标签，删除文章标签，更新文章标签详情视图（需要登录和博主权限）
class ArticleTagManipulateView(APIView):
    # 需要登录以及博主权限
    authentication_classes = [KennyAuthentication, ]
    permission_classes = [BloggerPermission, ]

    # 增加文章标签 没啥用还是写着吧
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000}
        # pk只用于put与delete
        pk = kwargs.get('pk')
        if pk:
            ret['code'] = 4005
            ret['error'] = '此api不存在'
            return Response(ret)
            # return Response(ret, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        ser = articleserializer.ArticleTagSerializer(data=request.data)
        if ser.is_valid():
            try:
                ser.save()
                ret['data'] = ser.data
                return Response(ret)
            except Exception as e:
                ret['code'] = 2000
                ret['error'] = '新增标签失败！'
                return Response(ret)
                # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    # 修改文章标签
    def put(self, request, *args, **kwargs):
        ret = {'code': 1000}
        # pk只用于put与delete
        pk = kwargs.get('pk')
        if not pk:
            ret['code'] = 4005
            ret['error'] = '此api不存在'
            return Response(ret)
            # return Response(ret, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        tag = models.ArticleTag.objects.filter(id=pk).first()
        if not tag:
            ret['code'] = 4004
            ret['error'] = '该标签不存在或已被删除！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_404_NOT_FOUND)
        ser = articleserializer.ArticleTagSerializer(tag, data=request.data,partial=True)
        if ser.is_valid():
            try:
                ser.save()
                ret['data'] = ser.data
                return Response(ret)
            except Exception as e:
                ret['code'] = 2000
                ret['error'] = '标签修改失败！'
                return Response(ret)
                # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            ret['code'] = 4001
            ret['error'] = ser.errors
            return Response(ret)
            # return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    # 删除标签
    def delete(self, request, *args, **kwargs):
        ret = {'code': 1000}
        # pk只用于put与delete
        pk = kwargs.get('pk')
        if not pk:
            ret['code'] = 4005
            ret['error'] = '此api不存在'
            return Response(ret)
            # return Response(ret, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        tag = models.ArticleTag.objects.filter(id=pk).first()
        if not tag:
            ret['code'] = 4004
            ret['error'] = '该栏目不存在或已被删除！'
            return Response(ret)
            # return Response(ret, status=status.HTTP_404_NOT_FOUND)
        try:
            ser = articleserializer.ArticleTagSerializer(instance=tag, many=False)
            ret['data'] = ser.data
            tag.delete()
            return Response(ret)
        except Exception as e:
            ret.pop('data')
            ret['code'] = 2000
            ret['error'] = '标签删除失败'
            return Response(ret)
            # return Response(ret, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
