from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# To list all publised posts 
def post_list(request):
    posts_list = Post.published.all()
    #paginate list of 3
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts= paginator.page(page_number)
    except PageNotAnInteger:
        # if page is not an integer
        posts = paginator.page(1)

    except EmptyPage:
        # if page number is out of the last page result
        posts= paginator.page(paginator.num_pages)

    context = {'posts':posts,}
    return render(request, 'blog/post/list.html', context )

# render post details
def post_detail(request, post):
    post = get_object_or_404(Post,  
                             status=Post.Status.PUBLISHED,
                             slug=post,
    )

    context = {'post':post,}
    return render(request, 'blog/post/detail.html', context)