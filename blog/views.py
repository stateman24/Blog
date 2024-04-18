from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.contrib.postgres.search import TrigramSimilarity


# To list all publised posts 
def post_list(request, tag_slug=None):
    posts_list = Post.published.all()
    tags = None
    if tag_slug:
        tags = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tags])
    # paginate list of 3
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # if page is not an integer
        posts = paginator.page(1)

    except EmptyPage:
        # if page number is out of the last page result
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, "tags":tags}
    return render(request, 'blog/post/list.html', context)


# render post details
def post_detail(request, post):
    post = get_object_or_404(Post,  
                             status=Post.Status.PUBLISHED,
                             slug=post)
    comments = post.comments.filter(active=True)
    form = CommentForm()

    post_tag_id = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tag_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tag=Count("tags")).order_by("same_tag", '-publish')[:4]
    context = {'post': post, 'comments': comments, 'form': form, "similar_posts": similar_posts}
    return render(request, 'blog/post/detail.html', context)


def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            # form pass validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}'s comment: {cd['comment']}"
            send_mail(subject, message, 'ajibewadannyboi@gmail.com', cd['to'])
            sent = True
    else:
        form = EmailForm()
    context = {'post': post, 'form': form, 'sent': sent}
    return render(request, 'blog/post/share.html', context)


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                similarity = TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')
    context = {'form': form, 'query': query, 'results': results}
    return render(request, 'blog/post/search.html', context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {'post': post, 'form': form, 'comment': comment}
    return render(request, 'blog/post/comment.html', context)

