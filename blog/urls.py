from django.urls import path
from .views import post_list, post_detail

#namespace for the app 'blog'
app_name = 'blog'


urlpatterns = [
    path('', post_list, name='post_list'),
    path('<slug:post>/', post_detail, name='post_detail'),
]
