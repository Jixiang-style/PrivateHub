"""renranapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path

import xadmin
xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

# 上文文件资源
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    re_path(r'media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    path(r'xadmin/', xadmin.site.urls),
    # path('admin/', admin.site.urls),
    path('stu/', include("students.urls")),
    path('users/', include("users.urls")),
    path('', include("home.urls")),
    path('oauth/', include("oauth.urls")),
    path('article/', include("article.urls")),
    path('payments/', include("payments.urls")),
    path('ots/', include("store.urls")),
]
