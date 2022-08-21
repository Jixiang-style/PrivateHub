from rest_framework import serializers
from .models import ArticleCollection
class CollectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCollection
        fields = ["id","name"]

    def validate_name(self, name):
        """验证数据"""
        # 如果当前有用户曾经过同一个文集,则报错
        # print(self.context) # 字典  {request:对象,view:对象,data_format: 字符串}
        user = self.context["request"].user
        try:
            ArticleCollection.objects.get(user=user,name=name)
            raise serializers.ValidationError("对不起, 当前文集名称已经被使用!~")
        except ArticleCollection.DoesNotExist:
            pass

        return name

    def create(self, validated_data):
        """保存数据"""
        try:
            collection = ArticleCollection.objects.create(
                name=validated_data.get("name"),
                user=self.context["request"].user,
                orders=0,
            )
            return collection
        except:
            raise serializers.ValidationError("对不起, 添加文集失败!~")

    def update(self, instance, validated_data):
        """修改数据"""
        instance.name = validated_data.get("name")
        instance.save()
        return instance


from .models import Article
from datetime import datetime
class ArticleModelSerializer(serializers.ModelSerializer):
    """文章的序列化器"""
    position = serializers.BooleanField(write_only=True, label="添加文章的位置")
    class Meta:
        model = Article
        fields = ["id","name","content","collection","position","is_public"]
        read_only_fields = ["id","name","content","is_public"]

    def create(self, validated_data):
        """保存数据"""
        name = datetime.now().strftime("%Y-%m-%d")
        collection = validated_data.get("collection")
        user = self.context["request"].user
        try:
            article = Article.objects.create(
                name=name,
                orders=0,
                user=user,
                collection=collection
            )
        except:
            raise serializers.ValidationError("对不起, 添加文章失败!")

        position = validated_data.get("position")
        if position:
            """如果是下方添加,则把id设置为orders为id"""
            article.orders = article.id
            article.save()
        return article

from rest_framework import serializers
from .models import ArticleImage
class ArticleImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = ("image",)

    def create(self, validated_data):
        user_id = self.context["request"].user.id
        instance = ArticleImage.objects.create(
            image=validated_data.get("image"),
            orders=0,
            user=user_id,
        )
        instance.group = str(instance.image).split("/")[0]
        instance.save()
        return instance

from users.models import User
class AuthorModelSerializer(serializers.ModelSerializer):
    """文章作者"""
    class Meta:
        model = User
        fields = ["id","nickname","avatar"] # 自己编写需要显示的字段即可

from .models import ArticleCollection
class CollectionInfoModelSerializer(serializers.ModelSerializer):
    """文集信息"""
    class Meta:
        model = ArticleCollection
        fields = ["id","name"] # 自己编写需要显示的字段即可

class ArticleInfoModelSerializer(serializers.ModelSerializer):
    user = AuthorModelSerializer()
    collection = CollectionInfoModelSerializer()
    class Meta:
        model = Article
        fields = [
            "name", "render","content", "user",
            "collection", "updated_time",
            "read_count", "like_count",
            "collect_count", "comment_count",
            "reward_count",
        ]