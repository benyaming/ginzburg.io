from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    content = models.TextField()

    created = models.DateTimeField(auto_now=True)
    archived = models.DateTimeField(blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')

    views = models.IntegerField(default=0)
    background = models.ImageField()

    objects = models.Manager

    @property
    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/posts/{self.id}'

    def increment_views(self):
        self.views += 1
        self.save()

