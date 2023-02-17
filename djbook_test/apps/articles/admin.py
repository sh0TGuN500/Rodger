from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Article, Choice, Comment, ArticleLike, CommentLike  # , File


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 2


class ArticleLikeInLine(admin.TabularInline):
    model = ArticleLike
    extra = 2


class CommentLikeInLine(admin.TabularInline):
    model = CommentLike
    extra = 2


class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('pub_date', 'up_date', 'like_count')
    fieldsets = [
        (None, {'fields': ['title']}),
        (_('Author name'), {'fields': ['user']}),
        (_('Date information'), {'fields': readonly_fields[0:1], 'classes': ['collapse']}),
        (_('Article text'), {'fields': ['text']}),
        (_('Tags'), {'fields': ['tag']}),
        (_('Likes'), {'fields': [readonly_fields[2]]})
    ]
    inlines = [ChoiceInline, CommentInline, ArticleLikeInLine]
    list_filter = ['pub_date']
    search_fields = ['title']


'''class FileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'file_name', 'upload_date']}),
    ]
    list_filter = ['file_name']
    search_fields = ['file_name']
    readonly_fields = ('file_hash',)'''


admin.site.register(Article, ArticleAdmin)
# admin.site.register(File, FileAdmin)
