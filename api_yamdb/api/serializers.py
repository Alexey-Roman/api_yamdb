from rest_framework import serializers

from users.models import User


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'username'
        )

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
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )
