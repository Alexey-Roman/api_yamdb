from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from rest_framework import filters, permissions, status
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import (CreateUserSerializer, GetTokenSerializer,
                             UserSerialiser, SelfEditSerializer,
                             CategorySerializer, GenreSerializer,
                             TitleReadSerializer, TitleWriteSerializer,)
from users.models import User
from reviews.models import Category, Genre, Title
from .permissions import AdministratorEdit, IsAnonymous
from .filters import TitleFilter
from .mixins import CreateListDestroyMixinSet


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели user. Эндпойнт /users/* """
    queryset = User.objects.all()
    serializer_class = UserSerialiser
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (AdministratorEdit,)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get', 'patch'],
        detail=False,
        serializer_class=SelfEditSerializer,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CreateUserViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """Вьюсет для регистрации пользователя"""
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if User.objects.filter(
                username=request.data.get('username'),
                email=request.data.get('email')
        ).exists():
            user = get_object_or_404(
                User,
                username=request.data.get('username')
            )
            response_data = request.data
        else:
            serializer.is_valid(raise_exception=True)
            user = User.objects.create(**serializer.validated_data)
            response_data = serializer.data
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=None,
            recipient_list=(user.email,),
            fail_silently=False,
        )
        return Response(response_data, status=status.HTTP_200_OK)


class GetTokenViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    """Вьюсет для валидации пользователя и передачи токена"""
    queryset = User.objects.all()
    serializer_class = GetTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(
                user,
                confirmation_code
        ) is False:
            message = {'confirmation_code': 'Неверный код подтверждения'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class CategoryViewSet(CreateListDestroyMixinSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyMixinSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAnonymous | AdministratorEdit]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer
