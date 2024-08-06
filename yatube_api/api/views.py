from rest_framework import viewsets, filters, permissions
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from posts.models import Group, Post, Follow
from .permissions import AuthorOrReadOnly
from .serializers import (
    GroupSerializer, PostSerializer, CommentSerializer, FollowSerializer
)


class BaseMixin:
    """Кастомный миксин для повторяющегося кода."""

    error = PermissionDenied('Изменение и удаление чужого контента запрещено!')
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, AuthorOrReadOnly,)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise self.error
        super().perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.author != self.request.user:
            raise self.error
        return super().perform_destroy(serializer)


class PostViewSet(BaseMixin, viewsets.ModelViewSet):
    """ViewSet для модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(BaseMixin, viewsets.ModelViewSet):
    """ViewSet для модели Comment."""

    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

    def get_queryset(self):
        return self.get_post().comments.all()


class FollowViewSet(viewsets.ModelViewSet):
    """Viewset для модели Follow."""

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Group, предназначенный только для чтения."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
