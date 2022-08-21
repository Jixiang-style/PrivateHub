from django.shortcuts import render
from tablestore import *
from renranapi.utils.tablestore import TableStore
# Create your views here.
from rest_framework.generics import ListAPIView
from .models import ArticleCollection
from .serializers import CollectionModelSerializer
from rest_framework.permissions import IsAuthenticated
class MyCollectionListAPIView(ListAPIView):
    """我的文集"""
    serializer_class = CollectionModelSerializer
    permission_classes = [IsAuthenticated] # 必须是登陆用户才能访问过来
    def get_queryset(self):
        user = self.request.user
        """重写queryset属性值"""
        ret = ArticleCollection.objects.filter(user=user).order_by("orders","-id")
        if len(ret)<1:
            # 当用户如果没有文集,在默认给用户创建2个文集
            collection1 = ArticleCollection.objects.create(
                user=user,
                name="日记本",
                orders=1,
            )

            collection2 = ArticleCollection.objects.create(
                user=user,
                name="随笔",
                orders=2,
            )

            ret = [
                {"id": collection1.pk, "name": collection1.name},
                {"id": collection2.pk, "name": collection2.name},
           ]

        return ret


from rest_framework.generics import CreateAPIView
class CollectionCreateAPIView(CreateAPIView):
    """添加文集"""
    serializer_class = CollectionModelSerializer
    permission_classes = [IsAuthenticated]

from rest_framework.generics import UpdateAPIView
class CollectionUpdateAPIView(UpdateAPIView):
    """修改文集"""
    queryset = ArticleCollection.objects.all()
    serializer_class = CollectionModelSerializer
    permission_classes = [IsAuthenticated]

from rest_framework.viewsets import GenericViewSet
from .models import Article
from .serializers import ArticleModelSerializer
from rest_framework.response import Response

class ArticleOfCollectionViewSet(GenericViewSet, ListAPIView,CreateAPIView):
    """当前文集的文章列表"""
    serializer_class = ArticleModelSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        collection_id = request.query_params.get("collection")
        user = request.user
        queryset = Article.objects.filter(is_delete=False, user=user, collection_id=collection_id).order_by("orders","-id")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

from rest_framework.views import APIView
from rest_framework import status
import logging

class ArticlePublicStatusAPIView(APIView):
    """切换文章的发布状态"""
    permission_classes = [IsAuthenticated]
    def put(self,request,pk):
        try:
            article = Article.objects.get(pk=pk, user=request.user)
        except Article.DoesNotExist:
            return Response("对不起,当前文章不存在!", status=status.HTTP_400_BAD_REQUEST)

        is_public = request.data.get("is_public")
        article.is_public = not not is_public
        article.pub_date  = None
        article.save()

        # 获取当前作者的粉丝列表
        fans_list = self.get_fans_list(article.user.id)
        if is_public:
            """在作者发布内容以后, 把feed推送粉丝"""
            ret = self.push_feed(article.user.id, article.id, fans_list)
            if not ret:
                logging.error("推送Feed失败!")

        return Response("操作成功!")

    def push_feed(self, author_id, message_id, fans_list):
        """推送Feed流"""
        put_row_items = []
        ts = TableStore()
        for fans in fans_list:
            primary_key = [  # ('主键名', 值),
                ('user_id', fans),  # 接收Feed的用户ID
                ('sequence_id', PK_AUTO_INCR),  # 如果是自增主键，则值就是 PK_AUTO_INCR
                ("sender_id", author_id),  # 发布Feed的用户ID
                ("message_id", message_id),  # 文章ID
            ]
            attribute_columns = [('recevice_time', datetime.now().timestamp()), ('read_status', False)]
            put_row_items.append( ts.add_all(primary_key, attribute_columns) )

        return ts.do_all("user_message_table", put_row_items)


    def get_fans_list(self, author_id):
        """获取作者的粉丝"""
        ts = TableStore()
        inclusive_start_primary_key = [
            ('user_id', author_id),
            ('follow_user_id', INF_MIN),
        ]

        # 范围查询的结束主键
        exclusive_end_primary_key = [
            ('user_id', author_id),
            ('follow_user_id', INF_MAX),
        ]
        ret = ts.get_all("user_relation_table",inclusive_start_primary_key, exclusive_end_primary_key)
        fans_list = []
        if len(ret) > 0:
            for item in ret:
                fans_list.append( item["follow_user_id"] )
        return fans_list

class ArticlechangeCollection(APIView):
    """移动文章"""
    permission_classes = [IsAuthenticated]
    def put(self,request,pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response("对不起,当前文章不存在!", status=status.HTTP_400_BAD_REQUEST)

        collection_id = request.data.get("collection_id")
        article.collection_id = int(collection_id)
        article.save()
        return Response("操作成功!")

class ArticleIntervalAPIView(APIView):
    """定时发布文章"""
    permission_classes = [IsAuthenticated]
    def put(self,request,pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response("对不起,当前文章不存在!", status=status.HTTP_400_BAD_REQUEST)

        pub_date = request.data.get("pub_date")
        article.pub_date = pub_date
        article.save()
        return Response("操作成功!")


class ArticeUpdateAPIView(APIView):
    """文章标题和内容修改保存"""
    permission_classes = [IsAuthenticated]
    def put(self,request,pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response("对不起,当前文章不存在!", status=status.HTTP_400_BAD_REQUEST)

        article.name = request.data.get("name")
        article.content = request.data.get("content")
        article.render = request.data.get("render")
        article.save()
        return Response("操作成功!")

from .models import ArticleImage
from .serializers import ArticleImageModelSerializer
class ArticleImageAPIView(CreateAPIView):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageModelSerializer


from .models import SpecialManager
class SpecialListAPIView(APIView):
    """我管理的专题列表"""
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        article_id = request.query_params.get("article_id")
        manage_list = SpecialManager.objects.filter(user=user)
        data = []
        for item in manage_list:
            try:
                # 查询当前专题下所有的文章列表是否存在当前文章
                item.special.post_article_list.get(article_id=article_id)
                status = True
            except SpecialArticle.DoesNotExist:
                status = False
            data.append({
                "id": item.special.id,
                "name": item.special.name,
                "image": item.special.image.url if item.special.image else "",
                "is_post": status, # 专题对于当前文章的收录状态
            })
        return Response(data)

from .models import Special,ArticlePostLog,SpecialArticle
from datetime import datetime
class ArticlePostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        """文章投稿"""
        user = request.user
        article_id = request.data.get("article_id")
        special_id = request.data.get("special_id")

        try:
            article = Article.objects.get(user=user, pk=article_id)
        except Article.DoesNotExist:
            return Response("对不起, 当前文章不存在!", status=status.HTTP_400_BAD_REQUEST)

        # 验证专题是否存在
        try:
            special = Special.objects.get(pk=special_id)
        except Special.DoesNotExist:
            return Response("对不起, 当前专题不存在!", status=status.HTTP_400_BAD_REQUEST)

        # 判断当前文章是否向专题投稿
        article_post_log_list = ArticlePostLog.objects.filter(special=special, article=article).order_by("-id")
        # 判断是否有投稿历史
        if len(article_post_log_list) > 0:
            # 查看最后一次投稿记录的审核状态
            if article_post_log_list[0].status != 2:
                return Response("对不起, 文章已经向当前专题投稿了!", status=status.HTTP_400_BAD_REQUEST)

        # 判断当前投稿人是否属于专题的管理员
        try:
            """专题管理员"""
            special_manage = SpecialManager.objects.get(user=user, special=special)
            ArticlePostLog.objects.create(
                user=user,
                special=special,
                article=article,
                status=1,
                manager=user.id,
                post_time=datetime.now(),
                orders=0,
            )

            SpecialArticle.objects.create(
                special=special,
                article=article,
                orders=0,
            )

        except SpecialManager.DoesNotExist:
            """并非管理员"""
            ArticlePostLog.objects.create(
                user=user,
                special=special,
                article=article,
                status=0,
                manager=user.id,
                post_time="",
                orders=0,
            )

        except:
            return Response("投稿失败!")

        return Response("投稿成功!")


from rest_framework.generics import RetrieveAPIView
from .serializers import ArticleInfoModelSerializer
from users.models import User
class ArticleInfoAPIView(RetrieveAPIView):
    """文章详情信息"""
    serializer_class = ArticleInfoModelSerializer
    queryset = Article.objects.filter(is_public=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 访问者没有登陆
        focus = 0 # 当前访问者没有登陆,默认没有关注
        # 访问者已经登陆
        user = request.user
        if isinstance(user, User):
            # 判断访问者是否曾经关注过作者
            author = instance.user
            # 如果访问者和文章作者是同一个人,则不存在关注
            if author.id == user.id:
                focus = -1
            else:
                # 从关系库中获取当前访问者与作者之间的关注关系
                ts = TableStore()
                data = ts.get_one(
                    "user_relation_table",
                    [('user_id', author.id), ('follow_user_id', user.id)])

                if data:
                    # 已经登陆并且关注了
                    print(data)
                    focus = 2
                else:
                    # 已经登陆了,没有关注
                    focus = 1
        ret = dict(serializer.data)
        ret["focus"] = focus
        return Response(ret)

class UserFocusAPIView(APIView):
    """关注和取消关注"""
    permission_classes = [IsAuthenticated]
    def post(self,request):
        # 关注者[粉丝]
        user = request.user
        # 作者
        author_id = request.data.get("author_id")
        try:
            User.objects.get(pk=author_id)
        except User.DoesNotExist:
            return Response("对不起, 您关注的用户不存在!", status=status.HTTP_400_BAD_REQUEST)

        if user.id == author_id:
            return Response("对不起, 您无法关注自己!", status=status.HTTP_400_BAD_REQUEST)

        # 获取关注状态[0表示取消关注,1表示关注]
        focus = request.data.get("focus")
        ts = TableStore()
        if focus:
            """关注"""
            ret = ts.add_one(
                "user_relation_table",
                [('user_id', author_id), ('follow_user_id', user.id)],
                [('focus_time', datetime.now().timestamp())]),
        else:
            """取消关注"""
            ret = ts.del_one("user_relation_table",
                [('user_id', author_id), ('follow_user_id', user.id)])

        if ret:
            return Response("操作成功!")
        else:
            return Response("操作失败!")