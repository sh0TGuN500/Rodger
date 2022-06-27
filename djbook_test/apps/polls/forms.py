from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Comment, Question


def text_validator(text):
    splitted_text = text.split()
    if len(splitted_text) >= 0 and not text.isspace():
        return ' '.join(splitted_text)
    else:
        return None


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
        data = text_validator(self.cleaned_data['comment_text'])
        if data:
            return data

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        else:
            raise ValidationError('This field must contain the text!')


class AddQuestionForm(forms.ModelForm):
    """Add auestion form"""

    class Meta:
        model = Question
        fields = ('question_title', 'question_text')
        widgets = {
            'question_title': forms.TextInput(attrs={'placeholder': 'Question title'}),
            'question_text': forms.Textarea(attrs={'cols': 35,
                                                   'rows': 3,
                                                   'minlength': 50,
                                                   'placeholder': 'Question text'})
        }
        labels = {
            'question_title': '',
            'question_text': ''
        }

    def clean_question_title(self):
        data = text_validator(self.cleaned_data['question_title'])
        if data:
            return data

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        else:
            raise ValidationError('This field must contain the text!')

    def clean_question_text(self):
        data = text_validator(self.cleaned_data['question_text'])
        if data:
            return data

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        else:
            raise ValidationError('This field must contain the text!')