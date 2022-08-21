from django.urls import path,re_path
from . import views
urlpatterns = [
    path("alipay/", views.AliPayAPIViewSet.as_view({"post":"post"})),
    path("alipay/result/", views.AliPayAPIViewSet.as_view({"get":"return_result","post":"notify_result"})),
]

