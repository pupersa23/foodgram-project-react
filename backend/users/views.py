from http import HTTPStatus

from django.shortcuts import get_list_or_404, get_object_or_404
from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework.response import Response

from api.permissions import IsAuthorOrReadOnly
from api.pagination import CustomPageNumberPagination
from users.models import Follow, User
from users.serializers import CustomUserCreateSerializer, FollowSerializer


class CreateUserView(UserViewSet):
    serializer_class = CustomUserCreateSerializer

    def get_queryset(self):
        return User.objects.all()


class SubscribeViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = FollowSerializer

    def get_queryset(self):
        return get_list_or_404(User, following__user=self.request.user)

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs.get('users_id')
        user = get_object_or_404(User, id=user_id)
        Follow.objects.create(
            user=request.user, following=user)
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs['users_id']
        user_id = request.user.id
        subscribe = get_object_or_404(
            Follow, user__id=user_id, following__id=author_id)
        subscribe.delete()
        return Response(HTTPStatus.NO_CONTENT)
