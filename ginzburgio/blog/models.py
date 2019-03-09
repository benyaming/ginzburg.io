from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f'{reverse("index")}?category={self.name}'


class Tag(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f'{reverse("index")}?tag={self.name}'


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    content = models.TextField()
    created = models.DateTimeField(auto_now=True)
    archived = models.DateTimeField(blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/posts/{self.id}'

    def increment_views(self):
        self.views += 1
        self.save()

    # def like(self):
    #     self.likes += 1
    #     self.save()
    #
    # def unlike(self):
    #     if self.likes > 0:
    #         self.likes -= 1


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    session = models.CharField(max_length=250)

    class Meta:
        unique_together = ('post', 'session')


