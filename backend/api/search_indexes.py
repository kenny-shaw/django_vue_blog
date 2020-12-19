from django.utils import timezone
from haystack import indexes
from api import models
# 计算指定对象的个数
from django.db.models import Count

# 原作者在代码中没有给出模型代码,这个模型里拥有的字段就是需要提供搜索的字段,建议保留模型字段中自增的主键字段id, 在我实际项目开发中发现如果不保留就无法实现搜索


# 索引模型类的名称为“模型类名称”+Index
class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    """索引数据模型类"""
    # 一般此字段约定为text
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')
    article_likes = indexes.IntegerField()

    # content=indexes.CharField(model_attr='content')
    # title=indexes.CharField(model_attr='title')
    def prepare_article_likes(self, obj):
        return obj.like_list.count()

    def get_model(self):
        """返回建立索引的模型类"""
        return models.Article

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.all()
