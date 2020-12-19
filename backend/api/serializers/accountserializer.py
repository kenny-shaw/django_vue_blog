from rest_framework import serializers
from api import models
from rest_framework.validators import UniqueValidator
# 使用django自带的密码加密解密类库
from django.contrib.auth.hashers import make_password, check_password
# 引入ContentType表，用于获取某个人的文章点赞对象（因为也有可能是评论）
from django.contrib.contenttypes.models import ContentType

# 用户管理序列化
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = "__all__"


# 用户注册序列化，用于校验数据
class RegisterValidateSerializer(serializers.Serializer):
    username = serializers.CharField(label='用户名', max_length=20, min_length=3, help_text='用户名',
                                     validators=[
                                         UniqueValidator(
                                             queryset=models.Account.objects.all(),
                                             message="该用户名已存在"
                                         )
                                     ],
                                     error_messages={
                                         ## 键值对，对应上面的限制条件，以及对应的提示
                                         "max_length": "最长20个字符",
                                         "min_length": "最短3个字符"
                                     })
    password = serializers.CharField(label='账号密码', max_length=20, min_length=5, help_text='账号密码',
                                     error_messages={"required": "请输入密码"})
    password2 = serializers.CharField(label='确认密码', max_length=20, min_length=5, help_text='确认密码',
                                      error_messages={"required": "请再次输入密码"},write_only=True)
    email = serializers.EmailField(label='邮箱', max_length=64, help_text='邮箱',
                                   validators=[
                                       UniqueValidator(
                                           queryset=models.Account.objects.all(),
                                           message="该邮箱已被注册"
                                       )
                                   ], required=False)
    gender = serializers.IntegerField(label='性别', help_text='性别', required=False)
    avatar = serializers.CharField(label='头像', max_length=256, help_text='头像', required=False)
    brief = serializers.CharField(label='简介', max_length=256, help_text='简介', required=False)
    job = serializers.CharField(label='职业', max_length=128, help_text='职业', required=False)
    company = serializers.CharField(label='公司', max_length=128, help_text='公司', required=False)

    # 对象级校验，检测输入的password与password2是否一致
    def validate(self, attrs):
        """检测输入的password与password2是否一致"""
        # 由于Account数据库中没有password2这一字段，所以校验后password2字段无法入库，因此对其进行删除
        password2 = attrs.pop('password2')
        if attrs['password'] != password2:
            raise serializers.ValidationError("两次输入密码不一致，请重新输入！")
        return attrs

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return models.Account.objects.create(**validated_data)


# 用户个人信息展示序列化以及修改序列化，用于校验数据
class UserInfoSerializer(serializers.ModelSerializer):
    # gender = serializers.CharField(source='get_gender_display')
    # role = serializers.CharField(source='get_role_display',read_only=True)
    class Meta:
        model = models.Account
        fields = ['id','role','username', 'email', 'gender', 'avatar', 'brief','job','company']
        extra_kwargs={
            'username': {'validators':[ UniqueValidator(queryset=models.Account.objects.all(),
                                             message="该用户名已存在")]
                         }
        }


# 用户个人粗略信息展示序列化，用于给别人查看,以及增加总点赞量、总阅读量等信息
class UserGeneralInfoSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display')
    role=serializers.CharField(source='get_role_display')
    article_counts=serializers.CharField(source='author_article.count')
    favorite_counts=serializers.CharField(source='user_favorite.count')
    # 获得的总点赞量（文章、评论，后续还有图片等等……）
    obtained_total_likes = serializers.SerializerMethodField()
    # 获得的文章总阅读量
    obtained_total_views=serializers.SerializerMethodField()
    # 向他人点赞数
    like_articles_count=serializers.SerializerMethodField()
    class Meta:
        model = models.Account
        fields = ['id','username', 'gender', 'avatar', 'brief',
                  'obtained_total_likes','obtained_total_views',
                  'date_joined','job','company','role','article_counts',
                  'favorite_counts','like_articles_count']

    def get_obtained_total_likes(self, obj):
        articles = models.Article.objects.filter(author=obj)
        # 使用一个列表，记录该作者的每篇文章的点赞量
        articles_likes = [article.like_list.count() for article in articles]
        comments = models.Comment.objects.filter(user=obj)
        # 使用一个列表，记录该作者的每个评论的点赞量
        comments_likes = [comment.like_list.count() for comment in comments]
        # 将二者的和返回
        return sum(articles_likes) + sum(comments_likes)
    def get_obtained_total_views(self,obj):
        articles = models.Article.objects.filter(author=obj)
        # 使用一个列表，记录该作者的每篇文章的点赞量
        articles_views = [article.total_views for article in articles]
        return sum(articles_views)
    def get_like_articles_count(self,obj):
        articletable = ContentType.objects.filter(model='article').first()
        articles=models.Like.objects.filter(user=obj,content_type=articletable)
        return articles.count()


# 用户密码修改序列化
class SetPasswordValidateSerializer(serializers.Serializer):
    oldpassword = serializers.CharField(label='账号原密码', max_length=20, min_length=5, help_text='账号原密码',
                                        error_messages={"required": "请输入原密码"})
    newpassword = serializers.CharField(label='账号新密码', max_length=20, min_length=5, help_text='账号密码',
                                        error_messages={"required": "请输入新密码"})
    newpassword2 = serializers.CharField(label='账号新密码', max_length=20, min_length=5, help_text='账号密码',
                                         error_messages={"required": "请再次输入新密码"})

    # 对象级校验，检测输入的password与password2是否一致
    def validate(self, attrs):
        """检测输入的两次密码是否一致，以及oldpassword与newpassword是否一致,新旧密码不能一致"""
        if attrs['newpassword'] != attrs['newpassword2']:
            raise serializers.ValidationError("两次输入密码不一致，请重新输入！")
        if attrs['oldpassword'] == attrs['newpassword']:
            raise serializers.ValidationError("新旧密码不能一致，请重新输入！")
        return attrs

    # 更新用户密码方法
    def update(self, instance, validated_data):
        #  不能使用make_password(validated_data.get('password',instance.password)) 防止不更新密码时 不停对原密码再加密
        instance.password = make_password(validated_data.get('newpassword')) if validated_data.get(
            'newpassword') else instance.password
        instance.save()
        return instance


# 密码重置数据校验序列化
class ReSetPasswordValidateSerializer(serializers.Serializer):
    newpassword = serializers.CharField(label='账号新密码', max_length=20, min_length=5, help_text='账号密码',
                                        error_messages={"required": "请输入新密码"})
    newpassword2 = serializers.CharField(label='账号新密码', max_length=20, min_length=5, help_text='账号密码',
                                         error_messages={"required": "请再次输入新密码"})

    # 对象级校验，检测输入的password与password2是否一致
    def validate(self, attrs):
        """检测输入的两次密码是否一致"""
        if attrs['newpassword'] != attrs['newpassword2']:
            raise serializers.ValidationError("两次输入密码不一致，请重新输入！")
        return attrs

    # 更新用户密码方法
    def update(self, instance, validated_data):
        instance.password = make_password(validated_data.get('newpassword', instance.password))
        instance.save()
        return instance


# 用户管理序列化
class AccountAdminSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(label='确认密码', max_length=20, min_length=5, help_text='确认密码',
    #                                   error_messages={"required": "请再次输入密码"}, write_only=True)

    class Meta:
        model = models.Account
        fields = "__all__"
        # fields = ["username", "password", "password2", "gender", "avatar", "role", "brief", "email"]
        extra_kwargs = {
            'username': {'validators': [UniqueValidator(queryset=models.Account.objects.all(),
                                                        message="该用户名已存在")]
                         },
            'email': {'validators': [UniqueValidator(queryset=models.Account.objects.all(),
                                                        message="该邮箱已被注册")]
                         }
        }
    # def validate(self, attrs):
    #     """检测输入的两次密码是否一致"""
    #     password2 = attrs.pop('password2')
    #     if password2 != attrs['password']:
    #         raise serializers.ValidationError("两次输入密码不一致，请重新输入！")
    #     return attrs

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return models.Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # validated_data.get为娶不到就取默认值
        instance.username = validated_data.get('username', instance.username)
        #  不能使用make_password(validated_data.get('password',instance.password)) 防止不更新密码时 不停对原密码再加密
        instance.password = make_password(validated_data.get('password')) if validated_data.get(
            'password') else instance.password
        instance.gender = validated_data.get('gender', instance.gender)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.role = validated_data.get('role', instance.role)
        instance.brief = validated_data.get('brief', instance.brief)
        instance.email = validated_data.get('email', instance.email)
        instance.job = validated_data.get('job', instance.job)
        instance.company = validated_data.get('company', instance.company)
        instance.save()
        return instance
