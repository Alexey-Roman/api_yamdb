from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import CreateUserSerializer, GetTokenSerializer
from users.models import User


class CreateUserViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=None,
            recipient_list=(user.email,),
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = GetTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
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
