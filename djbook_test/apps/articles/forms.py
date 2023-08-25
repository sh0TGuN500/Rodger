from django import forms
from django.utils.translation import gettext as _
import re

from .models import Comment, Article


def cleanhtml(raw_html):
    clean_re = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(clean_re, '', raw_html)
    return cleantext


def text_validator(origin_text: str, min_length: int = 0, max_length: int = 0):

    splitted_text: list = cleanhtml(origin_text.strip()).split()
    formated_text = ' '.join(splitted_text)
    if min_length:
        if not len(formated_text) >= min_length:
            return ''
    if max_length:
        if not len(formated_text) <= max_length:
            return ''
    if len(splitted_text) > 0 and not formated_text.isspace():
        return origin_text.strip()
    else:
        return ''


class CommentForm(forms.ModelForm):
    """Comments form"""

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'cols': 45,
                                          'rows': 3,
                                          'minlength': 4,
                                          'maxlength': 300,
                                          'placeholder': _('Your comment...')})
        }
        labels = {
            'text': '',
        }


class ArticleEditForm(forms.ModelForm):
    """Add article form"""

    class Meta:
        model = Article
        fields = ('title', 'text')
        widgets = {
            'title': forms.TextInput(attrs={'minlength': 5,
                                            'maxlength': 200}),
            'text': forms.Textarea(attrs={'minlength': 10,
                                          'maxlength': 9000})
        }
