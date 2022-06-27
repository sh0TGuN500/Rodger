from datetime import timedelta

from django.db import models
from django.utils import timezone

'''from django.contrib.postgres.fields import ArrayField
from storages.backends.sftpstorage import SFTPStorage
from hashlib import md5

file_storage = SFTPStorage()'''


class Question(models.Model):
    question_title = models.CharField('question title', max_length=200, unique=True)
    question_text = models.TextField('question text', max_length=9000)
    author_name = models.CharField('author name', max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_title

    def was_published_recently(self):
        now = timezone.now()
        return now - timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField('votes', default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.IntegerField('user')


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # ForeignKey привязка к классу Article, при удалении Article удаляется закрепленный за ним Comment
    author_name = models.CharField('author name', max_length=50, blank=False)
    comment_text = models.CharField('comment text', max_length=300, blank=False)

    def __str__(self):
        return self.author_name  # для отображения названия статьи


'''class Folder(models.Model):
    name = models.CharField('folder name', max_length=150)
    owner = models.CharField('user name', max_length=150)
    users = ArrayField(models.IntegerField())  # Users who have access


class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file_name = models.CharField('file name', max_length=255)
    file_hash = models.CharField(max_length=32, editable=False)
    upload_date = models.DateTimeField('date uploadnig')
    storage = models.FileField(upload_to='configurations',storage=file_storage, unique=True)

    def save(self, *args, **kwargs):
        self.file_hash = md5(self.file_name.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name'''
