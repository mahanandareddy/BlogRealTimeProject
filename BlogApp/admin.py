from django.contrib import admin
from BlogApp.models import Post,Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug', 'author', 'publish', 'created', 'updated','status']
    list_filter = ('status','created','publish','author')
    search_fields = ('title','body')
    prepopulated_fields = {"slug": ('title',)}
    raw_id_fields = ('author',)
    ordering = ['status', 'publish']
admin.site.register(Post,PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post','name','mail','body','created','updated','active']
    list_filter = ['active','created','updated']
    search_fields = ['name','mail','body']

admin.site.register(Comment,CommentAdmin)
