from django.test import TestCase
from django.urls import reverse

from ..models import Like, Post
from .test_models import test_vars, create_default_post


class PostDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_default_post()

    def test_view(self):
        response = self.client.get(reverse('post_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, test_vars['content'])

    def test_number_of_post_views(self):
        self.assertEqual(Post.objects.get(id=1).views, 0)
        self.client.get(reverse('post_detail', args=[1]))
        self.assertEqual(Post.objects.get(id=1).views, 1)
        self.client.get(reverse('post_detail', args=[1]))
        self.assertEqual(Post.objects.get(id=1).views, 2)


class PostListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_default_post()

    def test_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertContains(response, test_vars['title'])

    def test_view_categories(self):
        response = self.client.get(f'{reverse("index")}?category={test_vars["category"]}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertContains(response, test_vars['title'])

    def test_view_tags(self):
        response = self.client.get(f'{reverse("index")}?tag={test_vars["tags"]}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertContains(response, test_vars['title'])

    # TODO: test pagination


class CategoryListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_default_post()

    def test_view(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/category_list.html')
        self.assertContains(response, test_vars['category'])


class TagListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_default_post()

    def test_view(self):
        response = self.client.get(reverse('tags'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/tag_list.html')
        self.assertContains(response, test_vars['tags'])


class LikeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_default_post()

    def test_view(self):
        self.assertEqual(Like.objects.all().count(), 0)
        self.client.get(reverse('post_detail', args=[1]))
        response = self.client.post(reverse('like', args=[1]),
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Like.objects.all().count(), 1)

        response = self.client.delete(reverse('like', args=[1]),
                                      **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('like', args=[1]),
                                      **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 404)

        # TODO double like test;
        # django.db.transaction.TransactionManagementError: An error occurred in the
        # current transaction. You can't execute queries until the end
        # of the 'atomic' block.
