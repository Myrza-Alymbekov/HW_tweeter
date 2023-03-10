from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from tweeter import views

router = routers.DefaultRouter()
router.register('tweet', views.TweetViewSet)
router.register('comment', views.CommentViewSet)
router.register('user', views.UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include('rest_framework.urls')),

    path('api/', include(router.urls)),

    ]

