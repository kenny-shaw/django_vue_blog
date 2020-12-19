from django.contrib import admin

# Register your models here.
from api import models
admin.site.register(models.Account)
admin.site.register(models.UserAuthToken)
admin.site.register(models.ArticleColumn)
admin.site.register(models.ArticleTag)
admin.site.register(models.Article)
admin.site.register(models.Like)
admin.site.register(models.Comment)
admin.site.register(models.Favorite)
admin.site.register(models.FavoriteArticle)
admin.site.register(models.Lovers)
