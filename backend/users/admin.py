from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'id')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'
    list_filter = ('username', 'email')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    search_fields = ('user', )
    empty_value_display = '-пусто-'
    list_filter = ('user',)
