from django.urls import path
from django.views.decorators.cache import cache_page

from blogapp.apps import BlogappConfig
from blogapp.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogappConfig.name

urlpatterns = [
    path('blog', cache_page(60)(BlogListView.as_view()), name='blog_list'),
    path('blog_detail/<str:slug>/', cache_page(20)(BlogDetailView.as_view()), name='blog_detail'),
    path('blog/create/', cache_page(20)(BlogCreateView.as_view()), name='blog_create'),
    path('blog/<str:slug>/update/', cache_page(20)(BlogUpdateView.as_view()), name='blog_update'),
    path('blog/<str:slug>/delete/', cache_page(10)(BlogDeleteView.as_view()), name='blog_delete'),
]
