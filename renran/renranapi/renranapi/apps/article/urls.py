from django.urls import path,re_path
from . import views
urlpatterns = [
    path("collection/", views.MyCollectionListAPIView.as_view()),
    path("collect/", views.CollectionCreateAPIView.as_view()),
    re_path("^collect/(?P<pk>\d+)/$", views.CollectionUpdateAPIView.as_view()),
    path("", views.ArticleOfCollectionViewSet.as_view({"get":"list"})),
    re_path("^public/(?P<pk>\d+)/$", views.ArticlePublicStatusAPIView.as_view()),
    re_path("^move/(?P<pk>\d+)/$", views.ArticlechangeCollection.as_view()),
    re_path("^interval/(?P<pk>\d+)/$", views.ArticleIntervalAPIView.as_view()),
    re_path("^save/(?P<pk>\d+)/$", views.ArticeUpdateAPIView.as_view()),
    path("image/", views.ArticleImageAPIView.as_view()),
    path("special/list/", views.SpecialListAPIView.as_view()),
    path("post/", views.ArticlePostAPIView.as_view()),
    re_path("^(?P<pk>\d+)/$", views.ArticleInfoAPIView.as_view()),
    path("focus/", views.UserFocusAPIView.as_view()),
]