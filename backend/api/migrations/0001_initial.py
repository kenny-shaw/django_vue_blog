# Generated by Django 2.2 on 2020-08-13 16:26

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='用户名')),
                ('email', models.EmailField(blank=True, max_length=64, null=True, unique=True, verbose_name='邮箱')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
                ('gender', models.SmallIntegerField(choices=[(1, '保密'), (2, '男'), (3, '女')], default=1, verbose_name='性别')),
                ('avatar', models.CharField(blank=True, default='1.png', max_length=256, null=True, verbose_name='头像')),
                ('role', models.SmallIntegerField(choices=[(1, '普通用户'), (2, '管理员'), (3, '博主')], default=1, verbose_name='角色')),
                ('brief', models.TextField(blank=True, default='这个人很懒哦~', max_length=256, null=True)),
                ('job', models.CharField(blank=True, max_length=128, null=True, verbose_name='职业')),
                ('company', models.CharField(blank=True, max_length=128, null=True, verbose_name='公司')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='文章标题')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('avatar', models.CharField(blank=True, max_length=256, null=True, verbose_name='文章标题图')),
                ('total_views', models.PositiveIntegerField(default=0, verbose_name='文章浏览量')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='文章创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='最后创建时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_article', to='api.Account', verbose_name='作者')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleColumn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True, verbose_name='栏目名称')),
                ('brief', models.CharField(blank=True, default='暂无栏目简介~', max_length=256, null=True, verbose_name='栏目简介')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='栏目创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True, verbose_name='标签名称')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='标签创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True, verbose_name='收藏夹标题')),
                ('brief', models.CharField(blank=True, default='暂无收藏夹简介~', max_length=256, null=True, verbose_name='收藏夹简介')),
                ('avatar', models.CharField(blank=True, default='1.png', max_length=256, null=True, verbose_name='收藏夹标题图')),
                ('createdorupdated', models.DateTimeField(auto_now=True, verbose_name='最后创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='UserAuthToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255, unique=True)),
                ('created_or_updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_like', to='api.Account', verbose_name='点赞用户')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link_to_favorite', to='api.Article')),
                ('favorite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Favorite')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='favorite',
            name='article',
            field=models.ManyToManyField(related_name='article_favorite', through='api.FavoriteArticle', to='api.Article', verbose_name='收藏夹文章'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorite', to='api.Account', verbose_name='用户'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('object_id', models.PositiveIntegerField()),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='api.Comment', verbose_name='父评论')),
                ('reply_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replied_comment', to='api.Account', verbose_name='被回复者')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Account', verbose_name='评论用户')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='article',
            name='column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='column_article', to='api.ArticleColumn', verbose_name='文章栏目'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(related_name='tag_article', to='api.ArticleTag', verbose_name='文章标签'),
        ),
    ]