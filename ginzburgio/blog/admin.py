from django.contrib import admin

from .models import Post, Category, Tag


admin.site.register(Post, Category, Tag)
