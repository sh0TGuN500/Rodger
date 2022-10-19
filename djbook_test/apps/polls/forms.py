from django import forms
from django.core.exceptions import ValidationError

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
        return origin_text.strip()
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
                                                  'minlength': 4,
                                                  'maxlength': 300,
                                                  'placeholder': 'Your comment...'})
        }
        labels = {
            'comment_text': 'Your comment:\n',
        }

    def clean_comment_text(self):
        data = text_validator(self.cleaned_data['comment_text'], min_length=4, max_length=300)
        if data:
            return data
        else:
            raise ValidationError('Comment field must contain the text!')


class AddQuestionForm(forms.ModelForm):
    """Add question form"""

    class Meta:
        model = Question
        fields = ('question_title', 'question_text')
        widgets = {
            'question_title': forms.TextInput(attrs={'minlength': 5,
                                                     'maxlength': 200}),
            'question_text': forms.Textarea(attrs={'minlength': 10,
                                                   'maxlength': 9000})
    }

    def clean_question_title(self):
        data = text_validator(self.data['question_title'], min_length=5, max_length=200).upper()
        if data:
            return data
        else:
            raise ValidationError('Title field must contain the text!')

    def clean_question_text(self):
        print(f'clean text')
        data = text_validator(self.data['question_text'], min_length=10, max_length=9000)
        if data:
            return data
        else:
            raise ValidationError('Text field must contain the text!')


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
