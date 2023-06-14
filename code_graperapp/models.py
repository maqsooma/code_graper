from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Add custom fields
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)