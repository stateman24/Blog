from django.shortcuts import render, get_list_or_404
from .models import Post

# To list all publised posts 
def post_list(request):
    post = Post.published.all()
    context = {'post':post}
    render(request, 'blog/post/list.html', context)

def post_detail(request, id):
    post = get_list_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    context = {'post':post}
    render(request, 'blog/post/detail.html', context)