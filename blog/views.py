from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CommentForm, PostForm
from .models import Comment, Like, Post


class RolePermissionMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if user.groups.filter(name='Moderator').exists():
            return True
        post = getattr(self, 'object', None)
        if post is None and hasattr(self, 'get_object'):
            try:
                post = self.get_object()
            except Exception:
                post = None
        if post and post.author == user:
            return True
        return False


class AuthorOrModeratorMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (
            user.is_superuser
            or user.groups.filter(name__in=['Author', 'Moderator']).exists()
        )


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related('author')

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('HX-Request') == 'true':
            return render(self.request, 'blog/post_list_items.html', context, **response_kwargs)
        return super().render_to_response(context, **response_kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        queryset = Post.objects.select_related('author').prefetch_related('comments__author', 'likes')
        if self.request.user.is_authenticated and (
            self.request.user.is_superuser
            or self.request.user.groups.filter(name='Moderator').exists()
        ):
            return queryset
        if self.request.user.is_authenticated:
            return queryset.filter(Q(is_published=True) | Q(author=self.request.user))
        return queryset.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['liked'] = self.request.user.is_authenticated and self.object.likes.filter(user=self.request.user).exists()
        context['likes_count'] = self.object.likes.count()
        context['can_edit'] = self.request.user.is_authenticated and (
            self.request.user.is_superuser
            or self.request.user.groups.filter(name='Moderator').exists()
            or self.request.user == self.object.author
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(RolePermissionMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class PostDeleteView(RolePermissionMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class LikeToggleView(LoginRequiredMixin, View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
        if request.headers.get('HX-Request') == 'true':
            return render(request, 'blog/partials/like_button.html', {
                'post': post,
                'liked': post.likes.filter(user=request.user).exists(),
                'likes_count': post.likes.count(),
            })
        return redirect(post.get_absolute_url())


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, is_published=True)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            if request.headers.get('HX-Request') == 'true':
                return render(request, 'blog/partials/comment_item.html', {'comment': comment})
            return redirect(post.get_absolute_url())
        return redirect(post.get_absolute_url())
