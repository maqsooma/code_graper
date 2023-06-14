from rest_framework import serializers
from .models import User, Post, Like
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        email = validated_data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists.')
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=email,
            password=validated_data.get('password')
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token
        token['country'] = user.country
        token['city'] = user.city

        return token


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at']


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'created_at')
