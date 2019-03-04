from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post


class PostList(ListView):
    model = Post
    template_name = ''


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


# TODO urls
# TODO design
# TODO likes
# TODO templates
