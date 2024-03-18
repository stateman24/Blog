from django.urls import path
from . import views

#namespace for the app 'blog'
app_name = 'blog'


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:id>/', views.post_detail, name='post_detail'),
]
