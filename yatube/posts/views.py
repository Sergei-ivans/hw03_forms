from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post, Group, User
from .utils import func_paginator

NUMBER_LAST_ARTICLE = 25


def index(request):
    context = {'page_obj': func_paginator(request, Post.objects.all())}
    return render(
        request, 'posts/index.html', context
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    page_obj = func_paginator(request, posts)
    return render(
        request, 'posts/group_list.html',
        {'page_obj': page_obj, 'group': group}
    )


class JustStaticPage(TemplateView):
    template_name = 'app_name/just_page.html'


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    page_obj = func_paginator(request, posts)
    return render(
        request, 'posts/profile.html',
        {'page_obj': page_obj, 'author': user, 'posts': posts.count()}
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    pos_list = Post.objects.select_related('author').filter(author=post.author)
    return render(
        request, 'posts/post_detail.html',
        {'post': post, 'post_list': pos_list.count()}
    )


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author)
        return render(request, 'posts/create_post.html', {"form": form})
    return render(request, 'posts/create_post.html', {"form": form})


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    form = PostForm(instance=post)
    context = {
        "form": form,
        'is_edit': is_edit,
        'post': post,
    }
    return render(request, 'posts/create_post.html', context)
