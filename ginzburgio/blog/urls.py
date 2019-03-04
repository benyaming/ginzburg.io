from django.urls import path

from .views import PostList, PostDetail


urlpatterns = [
    path('posts/<int:pk>', PostDetail.as_view(), name='post_detail')
]
