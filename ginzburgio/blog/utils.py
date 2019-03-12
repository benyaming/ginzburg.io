import csv
from io import TextIOWrapper
from datetime import datetime

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.db.models.query import QuerySet
from django.forms import Form, FileField
from django.shortcuts import render, redirect

from .models import Post, Category, Tag


class ExportCsvMixin:
    """
    Additional functionality for csv exporting
    """
    def export_as_csv(self, request: HttpRequest, qs: QuerySet):
        meta = self.model._meta
        print(meta.fields)
        headers = [field.name for field in meta.fields]
        headers.append('tags')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=blog_posts.csv'
        writer = csv.writer(response)

        writer.writerow(headers)
        print(qs)
        for obj in qs:
            row = [getattr(obj, field) for field in headers[:-1]]
            row.append(','.join([tag.name for tag in obj.tags.all()]))
            writer.writerow(row)
        return response

    export_as_csv.short_description = 'Export selected as csv'


class CsvImportForm(Form):
    csv_file = FileField()


class ImportCsvMixin:
    """
        Additional functionality for csv importing
        """
    def import_csv(self, request: HttpRequest):
        if request.method == "POST":
            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding='utf-8')
            reader = csv.DictReader(csv_file)

            for row in reader:
                if row['archived'] == '':
                    row['archived'] = None

                try:
                    category = Category.objects.get(name=row['category'])
                except Category.DoesNotExist:
                    category = Category.objects.create(name=row['category'])

                tag_names = row['tags'].split(',')
                tags = []
                for tag_name in tag_names:
                    try:
                        tags.append(Tag.objects.get(name=tag_name))
                    except Tag.DoesNotExist:
                        tags.append(Tag.objects.create(name=tag_name))

                post_data = {
                    'title': row['title'],
                    'description': row['description'],
                    'content': row['content'],
                    'created': row['created'],
                    'archived': row['archived'],
                    'category': category,
                    'views': row['views']
                }
                post = Post.objects.create(**post_data)
                post.tags.set(tags)

            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "entities/csv_form.html", payload
        )


class ArchiveActionMixin:
    """
        Additional functionality for archiving and publishing posts
        """
    def archive(self, request: HttpRequest, qs: QuerySet):
        for obj in qs:
            obj.archived = datetime.now()
            obj.title += ' ARCHIVED'
            obj.save()

        self.message_user(request, "Posts have been archived!")

    def publicate(self, request: HttpRequest, qs: QuerySet):
        for obj in qs:
            obj.archived = None
            obj.title = obj.title.split(' ARCHIVED')[0]
            obj.save()

        self.message_user(request, "Posts have been publicated!")

    archive.short_description = 'Archive'
    publicate.short_description = 'Publicate'
