from django.db import models
# 引入ContentType
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# django-mptt
from mptt.models import MPTTModel, TreeForeignKey
from sortedm2m.fields import SortedManyToManyField


# Create your models here.
class Account(models.Model):
    """用户账户表"""
    username = models.CharField(verbose_name='用户名', max_length=20, unique=True)
    email = models.EmailField(verbose_name='邮箱', max_length=64, unique=True,default=None, null=True, blank=True)
    password = models.CharField(verbose_name='密码', max_length=256)
    gender_choices = ((1, '保密'), (2, '男'), (3, '女'))
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices, default=1)
    avatar = models.CharField(verbose_name='头像', max_length=256, null=True, blank=True)
    role_choices = ((1, '普通用户'), (2, '管理员'), (3, '博主'))
    role = models.SmallIntegerField(verbose_name='角色', choices=role_choices, default=1, null=True, blank=True)
    brief = models.TextField(max_length=256, default='这个人很懒哦~', null=True, blank=True)
    job = models.CharField(verbose_name='职业', max_length=128, null=True, blank=True)
    company = models.CharField(verbose_name='公司', max_length=128, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # 当获取Account对象时，显示其用户名username
    def __str__(self):
        return self.username
    # 邮箱unique且不为空



class UserAuthToken(models.Model):
    """用户Token表"""
    user = models.OneToOneField(to='Account', on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_or_updated = models.DateTimeField(auto_now=True)


class ArticleColumn(models.Model):
    """文章栏目表"""
    title = models.CharField(verbose_name='栏目名称', max_length=64, unique=True)
    brief = models.CharField(verbose_name='栏目简介', max_length=256, null=True, blank=True, default='暂无栏目简介~')
    created = models.DateTimeField(verbose_name='栏目创建时间', auto_now_add=True)

    # 当获取ArticleColumn对象时，显示其栏目名称title
    def __str__(self):
        return self.title


class ArticleTag(models.Model):
    """文章标签表"""
    title = models.CharField(verbose_name='标签名称', max_length=64, unique=True)
    avatar = models.CharField(verbose_name='标签标题图', max_length=256, null=True, blank=True)
    created = models.DateTimeField(verbose_name='标签创建时间', auto_now_add=True)

    # 当获取ArticleTag对象时，显示其标签名称title
    def __str__(self):
        return self.title


class Article(models.Model):
    """文章表"""
    author = models.ForeignKey(verbose_name='作者', to='Account', on_delete=models.CASCADE, related_name='author_article')
    title = models.CharField(verbose_name='文章标题', max_length=128)
    content = models.TextField(verbose_name='文章内容')
    content_text = models.TextField(verbose_name="文章文本内容")
    content_html = models.TextField(verbose_name="文章html内容")
    column = models.ForeignKey(verbose_name='文章栏目', to='ArticleColumn',
                               null=True, blank=True, on_delete=models.CASCADE, related_name='column_article')
    tag = models.ManyToManyField(verbose_name='文章标签', to='ArticleTag', related_name='tag_article')
    avatar = models.CharField(verbose_name='文章标题图', max_length=256, null=True, blank=True)
    total_views = models.PositiveIntegerField(verbose_name='文章浏览量', default=0)
    created = models.DateTimeField(verbose_name='文章创建时间', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='最后创建时间', auto_now=True)

    # 不会在数据库生成列，用于帮助进行点赞记录的查询
    like_list = GenericRelation('Like')
    # 不会在数据库生成列，用于帮助进行评论记录的查询
    comment_list = GenericRelation('Comment')

    # 当获取Article对象时，显示其文章名称title
    def __str__(self):
        return self.title


class Like(models.Model):
    """用户点赞表，采取ContentType"""
    user = models.ForeignKey(verbose_name='点赞用户', to='Account', on_delete=models.CASCADE, related_name="user_like")
    created = models.DateTimeField(verbose_name='点赞时间', auto_now_add=True)
    # 关联和点赞相关的表（文章、评论、相册等）
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 对应所关联的表中的id
    object_id = models.PositiveIntegerField()
    # 获取某条点赞的点赞内容，如文章表的某篇文章对象。不会在数据库生成列，只用于帮助查询前者所属对象和添加like记录
    content_object = GenericForeignKey('content_type', 'object_id')

    # 确定唯一点赞，表格和id相同时，不同重复点赞
    # class Meta:
    #     unique_together = (('content_type', 'object_id', 'user'),)


class Comment(MPTTModel):
    """
    用户评论表，采取ContentType，MPTT树形结构
    并且作为点赞表的一个content_object,拥有like_list字段
    兵器采取自关联字段，父评论与子评论自关联
    """
    user = models.ForeignKey(verbose_name='评论用户', to='Account', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='评论内容')
    parent = TreeForeignKey(verbose_name='父评论', to='self', null=True, blank=True, on_delete=models.CASCADE,
                            related_name='children')
    reply_to = models.ForeignKey(verbose_name='被回复者', to='Account', null=True, blank=True, on_delete=models.CASCADE,
                                 related_name='replied_comment')
    created = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    # 关联和评论相关的表（文章、相册等）
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    # 对应所关联的表中的id
    object_id = models.PositiveIntegerField()
    # 获取某条评论的评论内容，如文章表的某篇文章对象或是相册的某个照片。不会在数据库生成列，只用于帮助查询前者所属对象和添加Comment记录
    content_object = GenericForeignKey('content_type', 'object_id')
    # Like表的对象也有可能是评论，like_list能获取某评论的点赞数量
    like_list = GenericRelation('Like')


class Favorite(models.Model):
    """收藏夹表"""
    user = models.ForeignKey(verbose_name='用户', to='Account', on_delete=models.CASCADE, related_name='user_favorite')
    title = models.CharField(verbose_name='收藏夹标题', max_length=128, unique=True)
    brief = models.CharField(verbose_name='收藏夹简介', max_length=256, null=True, blank=True, default='暂无收藏夹简介~')
    article = models.ManyToManyField(verbose_name='收藏夹文章', to='Article',
                                     through='FavoriteArticle', related_name='article_favorite')
    avatar = models.CharField(verbose_name='收藏夹标题图', max_length=256, default='1.png', null=True, blank=True)
    createdorupdated = models.DateTimeField(verbose_name='最后创建时间', auto_now=True)

    # 当获取Favorite对象时，显示其名称title
    def __str__(self):
        return self.title



# 自定义收藏夹文章中间表
class FavoriteArticle(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='link_to_favorite', on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)

# 情侣表
class Lovers(models.Model):
    boy = models.CharField(verbose_name='男孩姓名', max_length=128)
    girl = models.CharField(verbose_name='女孩姓名', max_length=128)
    boyavatar=models.CharField(verbose_name='男孩头像', max_length=256, null=True, blank=True)
    girlavatar=models.CharField(verbose_name='女孩头像', max_length=256, null=True, blank=True)
    togetherdate = models.CharField(verbose_name='在一起时间',max_length=256)