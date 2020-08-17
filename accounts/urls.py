from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as views

urlpatterns = [
    path(
        "signup/<str:encoded_email>/<str:encrypted_hash>/",
        views.SignUp.as_view(),
        name="complete_signup",
    ),
    path("signup/", views.EnterEmail.as_view(), name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("about/", views.AboutUs.as_view(), name="about"),
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path("password_reset_done/", views.password_reset_done, name="password_reset_done"),
    path(
        "password_reset_confirm/<str:uidb64>/<str:token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
