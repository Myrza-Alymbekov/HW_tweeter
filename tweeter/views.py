from django.shortcuts import render
from rest_framework import authentication, viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from tweeter.models import Tweet, User, Comment
from tweeter.permissions import IsOwnerOrReadOnly
from tweeter.serializers import TweetSerializer, UserSerializer, CommentSerializer
from tweeter.mixins import LikedMixin, DislikedMixin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000


class TweetViewSet(LikedMixin, DislikedMixin, viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    pagination_class = ListPagination

    @action(methods=['POST'], detail=True)
    def comment(self, request, pk=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tweet=self.get_object(),
                            user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True)
    def view_comments(self, request, pk=None):
        queryset = Comment.objects.filter(tweet_id=self.get_object().id)
        serializer = CommentSerializer(queryset, many=True)

        return Response(serializer.data)


class CommentViewSet(LikedMixin, DislikedMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    pagination_class = ListPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
