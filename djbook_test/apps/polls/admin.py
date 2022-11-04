from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Question, Choice, Comment  # , File


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('pub_date', 'up_date')
    fieldsets = [
        (None, {'fields': ['question_title']}),
        (_('Author name'), {'fields': ['author_name']}),
        (_('Date information'), {'fields': readonly_fields, 'classes': ['collapse']}),
        (_('Question text'), {'fields': ['question_text']}),
        (_('Tags'), {'fields': ['tag']})
    ]
    inlines = [ChoiceInline, CommentInline]
    list_filter = ['pub_date']
    search_fields = ['question_title']


'''class FileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'file_name', 'upload_date']}),
    ]
    list_filter = ['file_name']
    search_fields = ['file_name']
    readonly_fields = ('file_hash',)'''


admin.site.register(Question, QuestionAdmin)
# admin.site.register(File, FileAdmin)
