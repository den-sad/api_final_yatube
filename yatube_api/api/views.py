from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework import filters

from posts.models import Post, Group, Follow, User
from .permissions import AuthorOrReadOnly
from .serializers import (PostSerializer, CommentSerializer, GroupSerializer,
                          FollowSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related(
        'author').all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = None
    serializer_class = CommentSerializer

    def get_post(self):
        post = get_object_or_404(
            Post,
            pk=self.kwargs.get('id'))
        return post

    def get_queryset(self):
        post = self.get_post()
        queryset = post.comments.select_related(
            'author')
        return queryset

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user,
                        post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = FollowSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        queryset = Follow.objects.select_related(
            'user', 'following').filter(user=user)
        return queryset

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        following_name = serializer.initial_data.get('following')
        following = User.objects.get(username=following_name)
        serializer.save(user=self.request.user, following=following)
