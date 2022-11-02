from django.contrib import admin

from .models import Question, Choice, Comment  # , File


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_title']}),
        ('Author name', {'fields': ['author_name']}),
        ('Question text', {'fields': ['question_text']}),
        ('Tags', {'fields': ['tag']})
    ]
    readonly_fields = ('pub_date', 'up_date')
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
