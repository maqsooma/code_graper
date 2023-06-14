from rest_framework.views import APIView
from .serializers import UserSerializer, PostSerializer, LikeSerializer
from rest_framework.response import Response
from .models import User, Post, Like
from django.db.models import Q
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
from rest_framework import generics
from .ip_geting import details

class SignupView(APIView):
    def post(self, requests):
        serializer = UserSerializer(data=requests.data)
        serializer.is_valid(raise_exception=True)
        user_s = serializer.save()
        user = User.objects.filter(id=user_s.id).first()
        address_details = details()
        user.city = address_details.get("city", '')
        user.country = address_details.get("country", '')
        user.save()

        return Response(serializer.data)


class LoginView(APIView):

    def post(self, requests):
        email = requests.data.get("username", '')
        password = requests.data.get("password", '')
        user = User.objects.filter(Q(email=email) | Q(username=email)).first()
        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(raw_password=password):
            raise AuthenticationFailed("Incorrect Password")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, "secret", algorithm="HS256").decode("utf-8")

        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "jwt": token
        }

        return response


class UserView(APIView):
    def get(self, requests):
        token = requests.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, "secret", algorithm=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        user = User.objects.filter(id=payload["id"]).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, requests):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {
            "message": "success"
        }
        return response


class PostListCreateView(generics.ListCreateAPIView):

    def post(self, request):
        token = request.COOKIES.get("jwt")
        try:
            payload = jwt.decode(token, "secret", algorithm=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        user = User.objects.filter(id=payload["id"]).first()
        post = Post.objects.create(user=user, content=request.data["content"])
        post.save()

        return Response("posts create successfully")

    def get(self, request):
        post_all = Post.objects.all()
        serializer = PostSerializer(post_all, many=True)
        return Response(serializer.data)


class LikeListCreateView(generics.ListCreateAPIView):
    def post(self, request, pk):
        token = request.COOKIES.get("jwt")
        try:
            payload = jwt.decode(token, "secret", algorithm=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        user = User.objects.filter(id=payload["id"]).first()
        post = Post.objects.filter(id=pk).first()
        like = Like.objects.create(user=user, post=post)
        like.save()

        return Response("like successfully")

    def get(self, request):
        token = request.COOKIES.get("jwt")
        try:
            payload = jwt.decode(token, "secret", algorithm=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        user = User.objects.filter(id=payload["id"]).first()
        post_like = Like.objects.filter(user=user)
        serializer = LikeSerializer(post_like, many=True)
        return Response(serializer.data)