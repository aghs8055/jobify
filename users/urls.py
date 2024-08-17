from django.urls import path
from users.views import login, logout, register, ProfileView, refresh

app_name = "users"

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("register/", register, name="register"),
    path("refresh/", refresh, name="refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
