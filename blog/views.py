from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailForm
from django.core.mail import send_mail



# To list all publised posts 
def post_list(request):
    posts_list = Post.published.all()
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

    context = {'posts': posts}
    return render(request, 'blog/post/list.html', context)


# render post details
def post_detail(request, post):
    post = get_object_or_404(Post,  
                             status=Post.Status.PUBLISHED,
                             slug=post)
    context = {'post': post}
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
    

