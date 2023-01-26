from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# from django.conf import settings
# settings.AUTH_USER_MODEL


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password2'
        )

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields didnt match.'}
            )
        return data

    def create(self, validated_data):
        # password2 kullanılmayacağı için dictten çıkardık
        validated_data.pop('password2')
        # password u daha sonra set etmek için değişkene atadık.
        password = validated_data.pop('password')
        # username=validate_data['username], email = va.......
        user = User.objects.create(**validated_data)
        # password ün encrypte olarak db ye kaydedilmesiniş sağlıyor.
        user.set_password(password)
        user.save()
        return user
