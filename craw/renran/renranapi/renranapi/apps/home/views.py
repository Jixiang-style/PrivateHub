from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from .models import Banner
from datetime import datetime
from .serializers import BannerModelSerializer
class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_delete=False,start_time__lte=datetime.now(), end_time__gte=datetime.now()).order_by("orders","-id")[:5]
    serializer_class = BannerModelSerializer

from .models import Nav
from .serializers import NavModelSerializer
class NavHeaderListAPIView(ListAPIView):
    queryset = Nav.objects.filter(is_show=True, is_delete=False, option=1,pid=None).order_by("orders","-id")[:8]
    serializer_class = NavModelSerializer

class NavFooterListAPIView(ListAPIView):
    queryset = Nav.objects.filter(is_show=True, is_delete=False, option=2,pid=None).order_by("orders","-id")[:8]
    serializer_class = NavModelSerializer

from rest_framework.views import APIView
from users.models import User
from article.models import Article
from rest_framework.response import Response
from .serializers import ArticleListModelSerializer
from renranapi.utils.tablestore import TableStore
from tablestore import *
class FeedAPIView(APIView):
    def get(self,request):
        if isinstance(request.user, User):
            """已登陆"""
            # 1. 根据当前用户id到未读池中查询上一次读取数据的最后一个自增ID,
            # 根据自增ID到存储库中获取Feed
            my_focus_list = self.focus_list(request.user.id)
            print(my_focus_list)
            # 1.1 没有Feed流内容[没有关注过任何人, 关注的作者没有新发布内容]

            # 1.2 有Feed流内容
        else:
            """未登陆"""
            # 2. 查询热门的数据出来
            start = int(request.query_params.get("start"))
            data = Article.objects.filter(is_public=True, is_delete=False).order_by("-reward_count","-like_count","-read_count","-id")[start:start+3]

        # serializer = ArticleListModelSerializer(instance=data, many=True)

        return Response([])

    def focus_list(self,follow_user_id):
        """当前用户的关注列表"""
        ts = TableStore()

        inclusive_start_primary_key = [
            ("user_id",2),
            ("follow_user_id", 1)
        ]

        exclusive_end_primary_key = [
            ("user_id", 2),
            ("follow_user_id", 3)
        ]
        print(follow_user_id)
        return ts.get_all("user_relation_table", inclusive_start_primary_key, exclusive_end_primary_key)
