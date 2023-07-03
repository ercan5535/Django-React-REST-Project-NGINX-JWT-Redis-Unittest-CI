from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.RegisterView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("refresh/", views.RefresfTokenView.as_view()),
    path("check/", views.CheckLoginStatus.as_view()),
    path("logout/", views.Logout.as_view()),
]
