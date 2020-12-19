# 引入serializers
from rest_framework import serializers
# 引入models模型类
from api import models


# 评论详情获取序列化，用以增加删除之后返回单条评论,也用于子评论序列化
class CommentReadDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    reply_to = serializers.CharField(source='reply_to.username', read_only=True)
    comment_likes = serializers.IntegerField(source='like_list.count')
    user_avatar = serializers.CharField(source='user.avatar', read_only=True)
    user_job = serializers.CharField(source='user.job', read_only=True)
    user_company = serializers.CharField(source='user.company', read_only=True)
    class Meta:
        model = models.Comment
        fields = ['id', 'user', 'user_avatar','user_job','user_company','content', 'reply_to', 'created', 'comment_likes']

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
        else:
            ret['likedbycuruser'] = 0
        return ret


# 评论列表获取序列化
class CommentReadListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    comment_likes = serializers.IntegerField(source='like_list.count')
    # children=serializers.SerializerMethodField()
    children = CommentReadDetailSerializer(instance='get_child', many=True)
    user_avatar=serializers.CharField(source='user.avatar', read_only=True)
    user_job = serializers.CharField(source='user.job', read_only=True)
    user_company = serializers.CharField(source='user.company', read_only=True)
    class Meta:
        model = models.Comment
        fields = ['id', 'user', 'user_avatar','user_job','user_company','content', 'created', 'children', 'comment_likes']

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
        else:
            ret['likedbycuruser'] = 0
        return ret
    # def get_children(self,obj):
    #     sub_comments=obj.get_children()
    #     if not sub_comments:
    #         return []
    #     return [{"id":comment.id,"user":comment.user.username,
    #              "content":comment.content,"created":comment.created,
    #              "reply_to":comment.reply_to.username,"comment_likes":comment.like_list.count()}
    #             for comment in sub_comments]


# 评论操作序列化（增加删除）
class CommentManipulateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"
        extra_kwargs = {
            # 外键
            'user': {'read_only': True},
            'parent': {'read_only': True},
            'reply_to': {'read_only': True},
            'content_object': {'read_only': True},

            'content_type': {'read_only': True},
            'object_id': {'read_only': True},
            'created': {'read_only': True},

        }
