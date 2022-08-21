from django.urls import path
from . import views
urlpatterns = [
    path("table/", views.TableAPIView.as_view()),
    path("data/", views.DataAPIViewSet.as_view({
        "post":"post",
        "get":"get",
    })),
    path("data2/", views.DataAPIViewSet.as_view({
        "get":"get2",
        "post":"post2",
    })),

]