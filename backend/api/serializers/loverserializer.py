# 引入serializers
from rest_framework import serializers
# 引入models模型类
from api import models
class LoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lovers
        fields = "__all__"


