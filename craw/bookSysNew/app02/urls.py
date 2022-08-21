from django.contrib import admin
from django.urls import path,re_path,include

from app02 import views

urlpatterns = [
    path('books/', views.books),
]
