from django.test import TestCase

from ..models import Post, Tag, Category, Like


test_vars = {
    'title': 'Test title',
    'description': 'Test description',
    'content': 'Test content',
    'category': 'Test category',
    'tags': 'Test tag'
}

test_post_data = {
    'title': test_vars['title'],
    'description': test_vars['description'],
    'content': test_vars['content'],
    'category': Category.objects.get(id=1)
}


def create_default_post():
    Category.objects.create(name=test_vars['category'])
    Tag.objects.create(name=test_vars['tags'])
    _ = Post.objects.create(**test_post_data)
    _.tags.set(Tag.objects.all())


class PostTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_default_post()

    def setUp(self):
        self.post = Post.objects.get(id=1)

    def test_post_title(self):
        self.assertEqual(self.post.title, test_vars['title'])

    def test_post_description(self):
        self.assertEqual(self.post.description, test_vars['description'])

    def test_post_content(self):
        self.assertEqual(self.post.content, test_vars['content'])

    def test_post_category(self):
        self.assertEqual(self.post.category.name, test_vars['category'])

    def test_post_tags(self):
        self.assertEqual(self.post.tags.get(id=1).name, test_vars['tags'])


class CategoryTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_default_post()

    def setUp(self):
        self.category = Category.objects.get(id=1)

    def test_category_name(self):
        self.assertEqual(self.category.name, test_vars['category'])

    def test_category_counts(self):
        self.assertEqual(Category.objects.all().count(), 1)
        self.assertEqual(self.category.posts.all().count(), 1)


class TagTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_default_post()

    def setUp(self):
        self.tag = Tag.objects.get(id=1)

    def test_tag_name(self):
        self.assertEqual(self.tag.name, test_vars['tags'])

    def test_tag_counts(self):
        self.assertEqual(Tag.objects.all().count(), 1)
        self.assertEqual(self.tag.posts.all().count(), 1)


class LikeTest(TestCase):

    def test_like(self):
        Category.objects.create(name=test_vars['category'])
        Tag.objects.create(name=test_vars['tags'])
        post = Post.objects.create(**test_post_data)
        post.tags.set(Tag.objects.all())

        self.like_params = {'post': post, 'session': 'test_session_key'}
        Like.objects.create(**self.like_params)

        self.assertEqual(Like.objects.all().count(), 1)
