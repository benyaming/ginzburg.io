from django.urls import path

from .views import PostList, PostDetail, LikeView


urlpatterns = [
    path('posts/<int:post_id>', PostDetail.as_view(), name='post_detail'),
    path('ajax/posts/<int:post_id>', LikeView.as_view(), name='like')
]
