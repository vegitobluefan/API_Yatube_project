from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (CurrentUserDefault, ModelSerializer,
                                        SlugRelatedField)

from posts.models import Comment, Follow, Group, Post, User


class AuthoredModelSerializerMixin(ModelSerializer):
    """Кастомный миксин для повторяющегося кода."""

    author = SlugRelatedField(slug_field='username', read_only=True)


class PostSerializer(AuthoredModelSerializerMixin):
    """Сериализатор для модели Post."""

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group',)


class CommentSerializer(AuthoredModelSerializerMixin):
    """Сериализатор для модели Comment."""

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

    def validate(self, attrs):
        if Follow.objects.filter(
            user__username=self.context['request'].user,
            following__username=attrs['following']
        ).exists():
            raise ValidationError('Вы уже подписаны на этого автора.')

        if self.context['request'].user == attrs['following']:
            raise ValidationError('Нельзя подписываться на самого себя.')
        return super().validate(attrs)

    class Meta:
        model = Follow
        fields = ('id', 'user', 'following',)
