from django.contrib import admin

from blogapp.models import Blog, Comment


@admin.register(Blog)
class AdminBlog(admin.ModelAdmin):
    list_display = ('pk', 'title', 'view_count',)
    list_filter = ('published',)
    search_fields = ('title', 'content',)


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ('pk', 'description', 'blog',)
    list_filter = ('blog',)
    search_fields = ('description',)
