from django.urls import path

from .views import PostList, PostDetail, LikeView, CategoryList, TagList


urlpatterns = [
    path('', PostList.as_view(), name='index'),
    path('tags', TagList.as_view(), name='tags'),
    path('categories', CategoryList.as_view(), name='categories'),
    path('posts/<int:post_id>', PostDetail.as_view(), name='post_detail'),
    path('ajax/posts/<int:post_id>', LikeView.as_view(), name='like')
]
