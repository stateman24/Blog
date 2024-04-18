from django.urls import path
from .views import post_list, post_detail, share_post, post_comment, post_search
from .sitemaps import PostSitemap
from django.contrib.sitemaps.views import sitemap
from .feeds import LatestPostsFeed

# namespace for the app 'blog'
app_name = 'blog'


sitemaps = {
    'posts': PostSitemap
}


urlpatterns = [
    path('', post_list, name='post_list'),
    path('<slug:post>/', post_detail, name='post_detail'),
    path('<int:post_id>/share/', share_post, name='share_post'),
    path('<int:post_id>/comment/', post_comment, name='post_comment'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('feeds.get/', LatestPostsFeed(), name='feeds'),
    path('search.get/', post_search, name='search'),
    path('sitemap.xml/', sitemap, {"sitemaps": sitemaps}, name='django.contrib.sitemaps.views'),
]
