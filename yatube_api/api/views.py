from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework import filters

from posts.models import Post, Group, Follow
from .permissions import AuthorOrReadOnly, ReadOnly
from .serializers import (PostSerializer, CommentSerializer, GroupSerializer,
                          FollowSerializer)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related(
        'author', 'group').prefetch_related('comments').all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = None
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_post(self):
        post = get_object_or_404(
            Post.objects.prefetch_related('comments'),
            pk=self.kwargs.get('id'))
        return post

    def get_queryset(self):
        queryset = self.get_post().comments.select_related(
            'author')
        return queryset

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user,
                        post=post)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed(
            'Созание групп только через админ-панель')


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        queryset = Follow.objects.filter(user=user)
        return queryset

    def validate(self, attrs):
        user = attrs['user']
        following_name = attrs['following']

        try:
            following = User.objects.get(username=following_name)
        except (Exception):
            raise ValidationError('Автор не найден')

        try:
            Follow.objects.get(
                user=user, following=following)
        except Follow.DoesNotExist:
            pass
        else:
            raise ValidationError(
                'Такая подписка уже существует')

        if user == following:
            raise ValidationError(
                'Нельзя подписаться на самого себя')
        return attrs

    def perform_create(self, serializer):
        following_name = serializer.initial_data.get('following')
        self.validate({'user': self.request.user,
                      'following': following_name, })
        following = User.objects.get(username=following_name)
        serializer.save(user=self.request.user, following=following)
