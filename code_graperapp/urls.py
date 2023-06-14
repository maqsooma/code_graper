from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('user/', views.UserView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('posts/', views.PostListCreateView.as_view(), name='post-list'),
    path('like/<int:pk>/', views.LikeListCreateView.as_view(), name='like-detail'),
    path('like/', views.LikeListCreateView.as_view(), name='like-detail'),
]
