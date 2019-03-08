from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.middleware.csrf import get_token

from .models import Post, Like


class PostList(ListView):
    model = Post
    template_name = ''


class PostDetail(DetailView):
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

    def post(self, request, post_id):
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

        likes = Like.objects.all().count()
        return JsonResponse({'msg': msg, 'likes': likes}, status=status)

    def delete(self, request, post_id):
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

        likes = Like.objects.all().count()
        return JsonResponse({'msg': msg, 'likes': likes}, status=status)
