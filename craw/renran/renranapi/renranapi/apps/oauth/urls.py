from django.urls import path
from . import views
urlpatterns = [
    path("qq/url/", views.OAuthQQAPIView.as_view()),
    path("qq/info/", views.QQUserInfoAPIView.as_view()),
]