from datetime import timedelta

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    name = models.CharField(
        _('tag name'),
        max_length=200,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(200)
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class Article(models.Model):
    title = models.CharField(
        _('article title'),
        max_length=200,
        unique=True,
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(200)
        ]
    )
    text = models.TextField(
        _('article text'),
        max_length=9000,
        validators=[
            MinLengthValidator(10),
            MaxLengthValidator(9000)
        ]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(_('publication date'), auto_now_add=True, null=False)
    tag = models.ManyToManyField(Tag, blank=True)
    up_date = models.DateTimeField(_('updating date'), null=True, blank=True)
    is_published = models.BooleanField(_('is published'), null=False, default=False)
    like_count = models.PositiveIntegerField(_('like counter'), default=0)

    def __str__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = _('Published recently?')

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')


class ArticleLike(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField(_('is like'))

    class Meta:
        verbose_name = _('Article like')
        verbose_name_plural = _('Article like')


class Choice(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(200)
        ]
    )
    votes = models.PositiveIntegerField(_('votes'), default=0)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Choice')
        verbose_name_plural = _('Choices')


class Vote(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)  # Foreignkey binding to the Article class,
    # when the Article is removed, the Comment assigned to it is removed
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(
        _('comment text'),
        max_length=300,
        blank=False,
        validators=[
            MinLengthValidator(4),
            MaxLengthValidator(300)
        ]
    )
    pub_date = models.DateTimeField(_('publication date'), auto_now_add=True)
    up_date = models.DateTimeField(_('updating date'), null=True, default=None)
    like_count = models.PositiveIntegerField(_('like counter'), default=0)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField(_('is like'))

    class Meta:
        verbose_name = _('Comment like')
        verbose_name_plural = _('Comment likes')


'''
class Folder(models.Model):
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
        return self.file_name
'''


'''
class FroalaModel(models.Model):
    name = models.CharField('Froala name', max_length=200)
    content = FroalaField()
    date = models.DateTimeField('Create data', auto_now=True)
'''


'''
from django.contrib.postgres.fields import ArrayField
from storages.backends.sftpstorage import SFTPStorage
from hashlib import md5

file_storage = SFTPStorage()
'''


'''
from avatar import models as avatar_models

def validate_file_size(value, max_size=5):
    max_size = max_size * 1024 * 1024
    filesize = value.size
    if filesize > max_size:
        raise ValidationError("The maximum file size that can be uploaded is 5MB.")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = avatar_models.Avatar()
    avatar = models.ImageField(upload_to='profile_pic/', default='articles/images/user_default.png',
                               validators=[validators.FileExtensionValidator(['jpg', 'jpeg', 'png']),
                                           validate_file_size])
'''
