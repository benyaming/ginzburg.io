from django.contrib import admin
from django.db.models import TextField
from django.urls import path

from .models import Post, Category, Tag
from .widgets import ContentWidget
from .utils import ExportCsvMixin, ImportCsvMixin, ArchiveActionMixin


class PostAdmin(admin.ModelAdmin, ExportCsvMixin, ImportCsvMixin, ArchiveActionMixin):
    """
    Overrides default Admin class. Add trumbowyg editor to post creating form;
    Adds links to import and export csv
    """
    formfield_overrides = {TextField: {'widget': ContentWidget}}
    actions = ['export_as_csv', 'archive', 'publicate']
    change_list_template = 'entities/post_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls


admin.site.register(Post, PostAdmin)
admin.site.register((Category, Tag))
