"""simpleblog_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog.views import index, post_list, post_detail, PostViewSet, UserViewSet, CategoryViewSet, User_ID_Search

router = DefaultRouter()
router.register('post_viewset', PostViewSet, 'post_model_viewset')
router.register('category', CategoryViewSet, 'category_viewset')
router.register('users', UserViewSet, "users")

urlpatterns = router.urls

urlpatterns.append(path('', index))
urlpatterns.append(path('posts/', post_list))
urlpatterns.append(path('posts/<int:pk>', post_detail))
urlpatterns.append(path('user_id_search/', User_ID_Search))

