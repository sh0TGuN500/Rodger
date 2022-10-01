from django.core.exceptions import ValidationError
from django import forms

from .models import Comment, Question


def text_validator(origin_text: str, min_length: int = 0, max_length: int = 0):
    splitted_text: list = origin_text.split()
    formated_text = ' '.join(splitted_text)
    if min_length:
        if not len(formated_text) >= min_length:
            return ''
    if max_length:
        if not len(formated_text) <= max_length:
            return ''
    if len(splitted_text) > 0 and not formated_text.isspace():
        return origin_text
    else:
        return ''


class CommentForm(forms.ModelForm):
    """Comments form"""

    class Meta:
        model = Comment
        fields = ('comment_text',)
        widgets = {
            'comment_text': forms.Textarea(attrs={'cols': 45,
                                                  'rows': 3,
                                                  'minlength': 3,
                                                  'placeholder': 'Your comment...'})
        }
        labels = {
            'comment_text': '',
        }

    def clean_comment_text(self):
        data = text_validator(self.cleaned_data['comment_text'], min_length=4, max_length=300)
        if data:
            return data

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        else:
            raise ValidationError('This field must contain the text!')


class AddQuestionForm(forms.ModelForm):
    """Add question form"""

    class Meta:
        model = Question
        fields = ('question_title', 'question_text')
        labels = {
            'question_title': '',
            'question_text': '',
        }

    def clean_question_title(self):
        data = text_validator(self.cleaned_data['question_title'])
        return data if data else ValidationError('This field must contain the text!')
        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.


'''class FroalaModelForm(forms.ModelForm):
    content = forms.CharField(widget=FroalaEditor)

    class Meta:
        model = FroalaModel
        fields = ('name', 'content')'''
