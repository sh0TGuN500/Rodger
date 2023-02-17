from django import forms
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from django.utils.translation import gettext as _
import re

from .models import Comment, Article


def text_validator(origin_text: str, min_length: int = 0, max_length: int = 0):
    clean_re = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    def cleanhtml(raw_html):
        cleantext = re.sub(clean_re, '', raw_html)
        return cleantext

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
            'text': _('Your comment\n'),
        }


'''
    def clean_comment_text(self):
        data = text_validator(self.cleaned_data['comment_text'], min_length=3, max_length=300)
        if data:
            return data
        else:
            raise ValidationError(_('Comment field must contain the text!'))
'''


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


'''
    def clean_article_title(self):
        data = text_validator(self.data['article_title'], min_length=5, max_length=200).upper()
        if data:
            return data
        else:
            raise ValidationError(_('should be the length between 5 and 200'))

    def clean_article_text(self):
        data = text_validator(self.data['article_text'], min_length=10, max_length=9000)
        if data:
            return data
        else:
            raise ValidationError(_('should be the length between 10 and 9000'))
'''

'''
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar',)

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            # validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is %s x %s pixels or smaller.' % (max_width, max_height))

            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, GIF or PNG image.')

            # validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar
'''

'''class FroalaModelForm(forms.ModelForm):
    content = forms.CharField(widget=FroalaEditor)

    class Meta:
        model = FroalaModel
        fields = ('name', 'content')'''

'''
CHOICES = [('1', 'First'), ('2', 'Second')]
choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
choice_field.choices
# [('1', 'First'), ('2', 'Second')]
choice_field.widget.choices
# [('1', 'First'), ('2', 'Second')]
choice_field.widget.choices = []
choice_field.choices = [('1', 'First and only')]
choice_field.widget.choices
'''
