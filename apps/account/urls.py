from django.urls import path # pyright: ignore[reportMissingModuleSource]

from rest_framework_simplejwt.views import TokenRefreshView # pyright: ignore[reportMissingImports]

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    CurrentUserView,
    StudentListView,
    StudentDetailView,
)


app_name = "account"

urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    path(
        "me/",
        CurrentUserView.as_view(),
        name="current-user",
    ),

    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),

    path(
    "students/",
    StudentListView.as_view(),
    name="student-list",
),

    path(
        "students/<int:pk>/",
        StudentDetailView.as_view(),
        name="student-detail",
    ),
]