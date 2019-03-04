from django.contrib import admin
from django.db.models import TextField

from .models import Post, Category, Tag
from .widgets import ContentWidget


class Admin(admin.ModelAdmin):
    formfield_overrides = {TextField: {'widget': ContentWidget}}


admin.site.register(Post, Admin)
admin.site.register((Category, Tag))
