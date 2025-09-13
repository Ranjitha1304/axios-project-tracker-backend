from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['is_trainer']


class UserRegisterSerializer(serializers.ModelSerializer):
    is_trainer = serializers.BooleanField(write_only=True, default=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_trainer']

    def create(self, validated_data):
        is_trainer = validated_data.pop('is_trainer', False)
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        profile = user.profile
        profile.is_trainer = is_trainer
        profile.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
