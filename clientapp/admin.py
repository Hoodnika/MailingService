from django.contrib import admin

from clientapp.models import User, Client


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'is_staff')
    list_filter = ('email', 'is_superuser')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'comment', 'owner')
    list_filter = ('email', 'owner')

