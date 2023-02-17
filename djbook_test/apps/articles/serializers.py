from django.utils import timezone
from rest_framework import serializers

from .models import Article, Comment, Tag, Vote, Choice, ArticleLike, CommentLike


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    up_date = serializers.DateTimeField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def update(self, instance, validated_data):
        # Custom update logic goes here
        up_date_value = validated_data.get('up_date', timezone.now())
        # Add the new field to the instance as an attribute
        instance.up_date = up_date_value
        # Call the super().update(instance, validated_data) to keep the original update logic as well
        instance = super().update(instance, validated_data)
        # Add additional logic for updating the instance if needed
        return instance

    def to_representation(self, instance):
        # Customize the serialization process
        representation = super().to_representation(instance)
        # Add a user field to the representation
        representation['user'] = str(instance.user)
        return representation


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class VoteListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vote
        fields = '__all__'

    def create(self, validated_data):
        # Perform additional processing or validation
        instance = super().create(validated_data)
        return instance


class ChoiceListSerializer(serializers.ModelSerializer):
    votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Choice
        fields = '__all__'


class ArticleLikeListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ArticleLike
        fields = '__all__'


class CommentLikeListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CommentLike
        fields = '__all__'


class ArticleListSerializer(serializers.ModelSerializer):
    pub_date = serializers.DateTimeField(read_only=True)
    up_date = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Article
        fields = ['id', 'title', 'text', 'user', 'tag', 'pub_date', 'up_date', 'like_count', 'is_published']

    def update(self, instance, validated_data):
        # Custom update logic goes here
        up_date_value = validated_data.get('up_date', timezone.now())
        # Add the new field to the instance as an attribute
        instance.up_date = up_date_value
        # Call the super().update(instance, validated_data) to keep the original update logic as well
        instance = super().update(instance, validated_data)
        # Add additional logic for updating the instance if needed
        return instance

    def to_representation(self, instance):
        # Customize the serialization process
        representation = super().to_representation(instance)
        # Add a user field to the representation
        representation['user'] = str(instance.user)
        return representation
