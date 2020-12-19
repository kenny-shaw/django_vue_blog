# 引入serializers
from rest_framework import serializers
# 引入models模型类
from api import models

# 文章标签序列化
class ArticleTagSerializer(serializers.ModelSerializer):
    article_counts =serializers.SerializerMethodField()
    class Meta:
        model = models.ArticleTag
        fields = "__all__"


    def get_article_counts(self,obj):
        queryset=obj.tag_article.all()
        return queryset.count()

# 文章栏目序列化
class ArticleColumnSerializer(serializers.ModelSerializer):
    # 获取栏目对应的文章id与title
    # articles = serializers.SerializerMethodField()
    class Meta:
        model = models.ArticleColumn
        fields = "__all__"
    # def get_articles(self,obj):
    #     queryset=obj.column_article.all()
    #     return [{'id':row.id,'title':row.title} for row in queryset]


# 文章作者序列化
class ArticleAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = "__all__"


# 文章列表粗略信息读取序列化
class ArticleReadListSerializer(serializers.ModelSerializer):
    # one2one/fk直接用source获取
    author = serializers.CharField(source='author.username')
    author_id = serializers.CharField(source='author.id')
    column = serializers.SerializerMethodField()
    # column=serializers.CharField(source='column.title')
    # m2m用SerializerMethodField方法获取
    tag = serializers.SerializerMethodField()

    article_likes=serializers.IntegerField(source='like_list.count')
    article_comments=serializers.IntegerField(source='comment_list.count')
    # likedbycuruser=serializers.IntegerField()
    class Meta:
        model = models.Article
        # fields = ['author','column','tag','title','avatar','total_views','article_likes']
        exclude=['content','content_text']
    # 防止column为空
    def get_column(self, obj):
        column = obj.column
        if column:
            return column.title
        return '暂无栏目~'

    # 获取tag的钩子函数,以数组方式展示
    def get_tag(self, obj):
        queryset = obj.tag.all()
        if queryset:
            return [row.title for row in queryset]
        else:
            return []

    # 文章是否被当前用户点赞、收藏
    def to_representation(self, instance):
        ret=super().to_representation(instance)
        # 判断是否存在当前用户（即是否有用户登录）
        if('curuser' in self.context):
            curuser=self.context['curuser']
            # 判断是否已被当前用户点赞
            like_obj=instance.like_list.filter(user=curuser).first()
            if like_obj:
                ret['likedbycuruser']=1
            else:
                ret['likedbycuruser'] = 0

            # 判断是否已被当前用户收藏,
            # 获取当前用户的所有收藏夹
            favorites=models.Favorite.objects.filter(user=curuser)
            # 是否已被当前用户收藏默认设置为0
            ret['favoritedbycuruser'] = 0
            # 遍历收藏夹
            for favorite in favorites:
                favoritearticle=favorite.article.filter(id=instance.id)
                if favoritearticle:
                    ret['favoritedbycuruser']=1
                    break
        else:
            ret['likedbycuruser'] = 0
            ret['favoritedbycuruser'] = 0
        return ret

# 文章详细信息读取序列化
class ArticleReadDetailSerializer(serializers.ModelSerializer):
    # one2one/fk直接用source获取
    author = serializers.CharField(source='author.username')
    column = serializers.SerializerMethodField()
    # column=serializers.CharField(source='column.title')
    # m2m用SerializerMethodField方法获取
    tag = serializers.SerializerMethodField()
    article_likes=serializers.IntegerField(source='like_list.count')
    article_comments=serializers.IntegerField(source='comment_list.count')
    author_id=serializers.IntegerField(source='author.id')
    class Meta:
        model = models.Article
        fields = "__all__"
        # exclude = ['content_text']

    # 防止column为空
    def get_column(self, obj):
        column = obj.column
        if column:
            return column.title
        return '暂无栏目~'

    # 获取tag的钩子函数
    def get_tag(self, obj):
        queryset = obj.tag.all()
        if queryset:
            return [row.title for row in queryset]
        else:
            return []
        # 文章是否被当前用户点赞、收藏

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 判断是否存在当前用户（即是否有用户登录）
        if ('curuser' in self.context):
            curuser = self.context['curuser']
            # 判断是否已被当前用户点赞
            like_obj = instance.like_list.filter(user=curuser).first()
            if like_obj:
                ret['likedbycuruser'] = 1
            else:
                ret['likedbycuruser'] = 0

            # 判断是否已被当前用户收藏,
            # 获取当前用户的所有收藏夹
            favorites = models.Favorite.objects.filter(user=curuser)
            # 是否已被当前用户收藏默认设置为0
            ret['favoritedbycuruser'] = 0
            # 遍历收藏夹
            for favorite in favorites:
                favoritearticle = favorite.article.filter(id=instance.id)
                if favoritearticle:
                    ret['favoritedbycuruser'] = 1
                    break
        else:
            ret['likedbycuruser'] = 0
            ret['favoritedbycuruser'] = 0
        return ret

# 文章操作序列化（增删改，与上面读取权限不同，是否需要登录不同）
class ArticleManipulateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = "__all__"
        extra_kwargs = {
            'total_views': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True},
            'author': {'read_only': True},
            'tag': {'read_only': True},
            'column': {'read_only': True},
        }
