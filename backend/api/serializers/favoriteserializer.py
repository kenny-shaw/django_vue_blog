# 引入serializers
from rest_framework import serializers
# 引入models模型类
from api import models
from api.serializers import articleserializer


class FavoriteReadSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    article_counts = serializers.CharField(source='article.count', read_only=True)
    user_id=serializers.CharField(source='user.id',read_only=True)
    # article = articleserializer.ArticleReadListSerializer(instance='article', many=True)
    class Meta:
        model = models.Favorite
        fields = ['id','user','user_id', 'title', 'brief', 'article_counts', 'avatar', 'createdorupdated']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ('curarticle' in self.context):
            curarticle = self.context['curarticle']
            # 查找收藏夹中是否有该文章
            favoritearticle=instance.article.filter(id=curarticle.id)
            if favoritearticle:
                ret['favoritedbycurfavorite'] = 1
            else:
                ret['favoritedbycurfavorite'] = 0
        else:
            ret['favoritedbycurfavorite'] = 0
        return ret


class FavoriteManipulateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Favorite
        fields = "__all__"
        extra_kwargs = {
            'user': {'read_only': True},
            'article': {'read_only': True},
            'createdorupdated': {'read_only': True}
        }
