from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post
from .consts import HOME_PAGE_POSTS_COUNT


def prepare_posts(queryset):

    return queryset.filter(
        is_published=True,
        pub_date__lte=timezone.now()
    ).select_related(
        'author',
        'location',
        'category'
    )


def index(request):
    post_list = prepare_posts(
        Post.objects.all().filter(category__is_published=True)
    )[:HOME_PAGE_POSTS_COUNT]

    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    post = get_object_or_404(
        prepare_posts(Post.objects.all()),
        pk=id,
        category__is_published=True
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = prepare_posts(category.posts.all())

    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': post_list
    })
