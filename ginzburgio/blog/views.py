from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.middleware.csrf import get_token

from .models import Post, Like, Tag, Category


class PostList(ListView):
    """
    View for index post list (optional with filters by tag or category)
    """
    model = Post
    template_name = 'blog/post_list.html'
    header_text = None
    queryset = Post.objects.filter(archived__isnull=True)
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['header_text'] = self.header_text
        return context

    def get(self, request, *args, **kwargs):
        if 'tag' in self.request.GET.keys():
            tag_name = self.request.GET['tag']
            tag = get_object_or_404(Tag, name=tag_name)
            self.queryset = Post.objects.filter(tags=tag)
            self.header_text = f'Все посты с тегом "{tag_name}"'

        elif 'category' in self.request.GET.keys():
            category_name = self.request.GET['category']
            category = get_object_or_404(Category, name=category_name)
            self.queryset = Post.objects.filter(category=category)
            self.header_text = f'Все посты в категории "{category_name}"'
        else:
            self.header_text = 'Все посты'
        self.paginate_by = 10

        return super().get(request, *args, **kwargs)


class CategoryList(ListView):
    """
    View for category list
    """
    model = Category
    template_name = 'blog/category_list.html'


class TagList(ListView):
    """
    View for tag list
    """
    model = Tag
    template_name = 'blog/tag_list.html'


class PostDetail(DetailView):
    """
    View for every post
    """
    model = Post
    template_name = 'blog/post_detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        session = self.request.session.session_key
        post = self.object
        try:
            Like.objects.get(post=post, session=session)
        except Like.DoesNotExist:
            pass
        else:
            context['liked'] = True
        return context

    def get(self, request, *args, **kwargs):
        request.session['init'] = 'ok'
        self.request.COOKIES['X-CSRFToken'] = get_token(self.request)
        render = super().get(request, *args, **kwargs)
        self.object.increment_views()
        return render


class LikeView(View):
    """
    View for ajax-only like-queries for 'like' and 'unlike' actions
    """
    def post(self, request, post_id):
        if not self.request.is_ajax():
            return HttpResponseBadRequest
        session = request.session.session_key
        post = get_object_or_404(Post, id=post_id)

        try:
            Like.objects.create(post=post, session=session)
        except IntegrityError:
            msg = 'Post already liked'
            status = 409
        else:
            msg = 'Liked!'
            status = 201

        likes = Like.objects.filter(post=post).count()
        return JsonResponse({'msg': msg, 'likes': likes}, status=status)

    def delete(self, request, post_id):
        if not self.request.is_ajax():
            return HttpResponseBadRequest
        session = request.session.session_key
        post = get_object_or_404(Post, id=post_id)
        try:
            like = Like.objects.get(post=post, session=session)
        except Like.DoesNotExist:
            status = 404
            msg = 'Not liked yet!'
        else:
            like.delete()
            status = 200
            msg = 'Unliked!'

        likes = Like.objects.filter(post=post).count()
        return JsonResponse({'msg': msg, 'likes': likes}, status=status)
