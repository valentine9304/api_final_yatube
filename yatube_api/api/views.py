from django.shortcuts import get_object_or_404

from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets, filters
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)

from .serializers import (PostSerializer, CommentSerializer,
                          FollowSerializer, GroupSerializer)

from .permission import IsAuthorOrReadOnly

from posts.models import Post, Follow, Group


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    http_method_names = ['get', 'post']
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
