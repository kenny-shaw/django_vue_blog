# Generated by Django 2.2 on 2020-08-16 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200815_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='content_text',
            field=models.TextField(default='aaa', verbose_name='文章文本内容'),
        ),
    ]
