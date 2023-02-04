from rest_framework import serializers

from users.models import User


class UserSerialiser(serializers.ModelSerializer):
    """Сериалайзер для модели user"""
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User


class SelfEditSerializer(serializers.ModelSerializer):
    """"Сериалайзер для модели user, в случае редактирования
    пользователем своих данных"""
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
        read_only_fields = ('role',)


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериалайзер при создании нового пользователя"""
    class Meta:
        fields = (
            'email',
            'username'
        )
        model = User

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Такой пользователь существует'
            )
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким email существует'
            )
        return data


class GetTokenSerializer(serializers.Serializer):
    """Сериалайзер для передаче токена при регистрации"""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )
