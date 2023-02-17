from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, PermissionDenied

from .models import Article, Comment, Choice, Vote, Tag, ArticleLike, CommentLike
from .permissions import ObjectOwnerPermission, GetPostOnlyPermission
from .serializers import ArticleListSerializer, CommentListSerializer, TagListSerializer, VoteListSerializer, \
    ChoiceListSerializer, ArticleLikeListSerializer, CommentLikeListSerializer


########################################################################################################################
################################################ DRF CRUD ##########################################################
########################################################################################################################


class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-pub_date')
    serializer_class = ArticleListSerializer
    permission_classes = (ObjectOwnerPermission,)


class CommentsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Comment.objects.all().order_by('-pub_date')
    serializer_class = CommentListSerializer
    permission_classes = (ObjectOwnerPermission,)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagListSerializer
    permission_classes = (GetPostOnlyPermission,)


class VotesViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all().order_by('article')
    serializer_class = VoteListSerializer
    permission_classes = (ObjectOwnerPermission,)

    def perform_create(self, serializer):
        article = Article.objects.get(id=self.request.data['article'])
        choice = Choice.objects.filter(pk=self.request.data['choice'], article=article)
        if choice.exists():
            if article.vote_set.filter(user=self.request.user).exists():
                raise ValidationError("You've already voted for this article.")
            else:
                choice.votes += 1
                serializer.save()
                choice.save()
        else:
            raise ValidationError("This choice is related to another article.")


class ChoicesViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all().order_by('article')
    serializer_class = ChoiceListSerializer

    def perform_create(self, serializer):
        article = Article.objects.get(id=self.request.data['article'])
        if article.user != self.request.user:
            raise PermissionDenied("You do not have permission to add choices to this article.")
        choice_text_exist = article.choice_set.filter(text=self.request.data['text']).exists()
        if choice_text_exist:
            raise ValidationError("The choice with this name already exists.")
        serializer.save(article=article)


class ArticleLikeViewSet(viewsets.ModelViewSet):
    queryset = ArticleLike.objects.all().order_by('article')
    serializer_class = ArticleLikeListSerializer
    permission_classes = (ObjectOwnerPermission,)

    def create(self, request, *args, **kwargs):
        article_id = request.data.get('article')
        user_id = request.user.id
        is_like = request.data.get('is_like')
        print(is_like)
        existing_like = ArticleLike.objects.filter(article=article_id, user=user_id).first()
        if existing_like:
            raise ValidationError("You've already liked/disliked this article.")
        if is_like:
            article = Article.objects.get(article_id)
            article.like_count += 1
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        article_id = instance.article.id
        user_id = request.user.id
        is_like = bool(request.data.get('is_like'))
        existing_like = ArticleLike.objects.filter(article=article_id, user=user_id).first()
        if not existing_like:
            raise ValidationError("You haven't liked/disliked this article yet.")
        elif existing_like.is_like != is_like:
            article = Article.objects.get(pk=article_id)
            article.like_count += 1 if is_like else -1
            article.save()
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        article_id = instance.article.id
        if instance.is_like:
            article = Article.objects.get(pk=article_id)
            article.like_count -= 1
            article.save()
        return super().destroy(request, *args, **kwargs)


class CommentLikeViewSet(viewsets.ModelViewSet):
    queryset = CommentLike.objects.all().order_by('comment')
    serializer_class = CommentLikeListSerializer
    permission_classes = (ObjectOwnerPermission,)

    def create(self, request, *args, **kwargs):
        comment_id = request.data.get('comment')
        user_id = request.user.id
        is_like = request.data.get('is_like')
        print(is_like)
        existing_like = CommentLike.objects.filter(comment=comment_id, user=user_id).first()
        if existing_like:
            raise ValidationError("You've already liked/disliked this comment.")
        if is_like:
            comment = Comment.objects.get(comment_id)
            comment.like_count += 1
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        comment_id = instance.comment.id
        user_id = request.user.id
        is_like = bool(request.data.get('is_like'))
        existing_like = CommentLike.objects.filter(comment=comment_id, user=user_id).first()
        if not existing_like:
            raise ValidationError("You haven't liked/disliked this comment yet.")
        elif existing_like.is_like != is_like:
            comment = Comment.objects.get(pk=comment_id)
            comment.like_count += 1 if is_like else -1
            comment.save()
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        comment_id = instance.comment.id
        if instance.is_like:
            comment = Comment.objects.get(pk=comment_id)
            comment.like_count -= 1
            comment.save()
        return super().destroy(request, *args, **kwargs)