# Generated by Django 2.2 on 2020-10-20 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20201016_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='content_html',
            field=models.TextField(default=1, verbose_name='文章html内容'),
            preserve_default=False,
        ),
    ]
