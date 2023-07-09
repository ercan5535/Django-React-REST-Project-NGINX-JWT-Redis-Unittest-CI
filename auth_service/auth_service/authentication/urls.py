from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("refresh/", views.RefresfTokenView.as_view(), name="refresh_token"),
    path("check/", views.CheckLoginStatus.as_view(), name="check_access_token"),
    path("logout/", views.Logout.as_view(), name="logout"),
]
