# 引入serializers
from rest_framework import serializers
# 引入models模型类
from api import models
from rest_framework.validators import UniqueTogetherValidator
class LikeSerializer(serializers.ModelSerializer):
    user=serializers.CharField(source='user.username',read_only=True)
    content_type=serializers.CharField(source='content_type.model',read_only=True)
    class Meta:
        model = models.Like
        fields = "__all__"
        extra_kwargs={
            'user': {'read_only': True},
            'content_object': {'read_only': True},
            'content_type': {'read_only': True},
            'object_id': {'read_only': True},
        }
        # validators=[UniqueTogetherValidator(queryset=models.Like.objects.all(),fields=('user','content_type','object_id'),message='您已经点赞了哟')]