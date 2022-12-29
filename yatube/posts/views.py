from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Group, User

from django.views.generic.base import TemplateView

from .forms import PostForm

from django.contrib.auth.decorators import login_required

NUMBER_LAST_ARTICLE = 25


def index(request):
    posts = Post.objects.all()[:NUMBER_LAST_ARTICLE]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request, 'posts/index.html', {'posts': posts, 'page_obj': page_obj})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)[:NUMBER_LAST_ARTICLE]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/group_list.html',
                  {'posts': posts, 'group': group, 'page_obj': page_obj})


class JustStaticPage(TemplateView):
    template_name = 'app_name/just_page.html'


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    posts_count = posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts_count': posts_count,
        'page_obj': page_obj,
        'author': user,
        'posts': posts,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    pos_list = Post.objects.select_related('author').filter(author=post.author)
    posts_count = pos_list.count()
    context = {
        'post': post,
        'posts_count': posts_count,
        'post_list': pos_list
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author)
        return render(request, 'posts/create_post.html', {"form": form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {"form": form})


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
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
