from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Article, Choice, Comment, ArticleLike, CommentLike, Tag  # , File


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 2
    readonly_fields = ('up_date', 'pub_date')


class ArticleLikeInLine(admin.TabularInline):
    model = ArticleLike
    extra = 2


class CommentLikeInLine(admin.TabularInline):
    model = CommentLike
    extra = 2


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('pub_date', 'up_date', 'like_count', 'user')
    fieldsets = [
        (None, {'fields': ['title']}),
        (_('Author name'), {'fields': [readonly_fields[3]]}),
        (_('Date information'), {'fields': readonly_fields[0:1]}),
        (_('Is published?'), {'fields': ['is_published']}),
        (_('Article text'), {'fields': ['text']}),
        (_('Tags'), {'fields': ['tag']}),
        (_('Likes'), {'fields': [readonly_fields[2]]})
    ]
    inlines = [ChoiceInline, CommentInline, ArticleLikeInLine]
    list_filter = ['pub_date']
    search_fields = ['title']
    list_display = ['title', 'is_published']
    list_editable = ('is_published',)

    actions = ['make_true', 'make_false']

    def make_true(self, request, queryset):
        queryset.update(is_published=True)

    make_true.short_description = "Make True for each"

    def make_false(self, request, queryset):
        queryset.update(is_published=False)

    make_false.short_description = "Make False for each"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


'''class FileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'file_name', 'upload_date']}),
    ]
    list_filter = ['file_name']
    search_fields = ['file_name']
    readonly_fields = ('file_hash',)'''

# admin.site.register(File, FileAdmin)
