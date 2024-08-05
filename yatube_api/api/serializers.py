from rest_framework.serializers import (
    ModelSerializer, SlugRelatedField, CurrentUserDefault
)

from posts.models import Group, Post, Comment, Follow, User


class PostSerializer(ModelSerializer):
    """Сериализатор для модели Post."""

    author = SlugRelatedField(slug_field='username', read_only=True,)

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group',)


class CommentSerializer(ModelSerializer):
    """Сериализатор для модели Comment."""

    author = SlugRelatedField(slug_field='username', read_only=True,)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created',)
        read_only_fields = ('post',)


class GroupSerializer(ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description',)


class FollowSerializer(ModelSerializer):
    """Сериализатор для модели Follow."""

    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault()
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('id', 'user', 'following',)
