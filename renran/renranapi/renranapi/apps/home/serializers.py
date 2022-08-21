from rest_framework import serializers
from .models import Banner
class BannerModelSerializer(serializers.ModelSerializer):
    """轮播图序列化器"""
    class Meta:
        model = Banner
        fields = ["image","link"]


from .models import Nav
class NavModelSerializer(serializers.ModelSerializer):
    """导航菜单序列化器"""
    class Meta:
        model = Nav
        fields = ["name","link","is_http","son_list"]

from rest_framework import serializers
from article.models import Article
from users.models import User
class ArticleAuthorModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id","nickname"]
        model = User
class ArticleListModelSerializer(serializers.ModelSerializer):
    user = ArticleAuthorModelSerializer()
    class Meta:
        model = Article
        fields = ["id","name","content","user","like_count","reward_count","comment_count"]