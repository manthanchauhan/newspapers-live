from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as views

urlpatterns = [
    path('signup/<str:encoded_email>/<str:encrypted_hash>/', views.SignUp.as_view(), name='complete_signup'),
    path('signup/', views.EnterEmail.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registeration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('about/', views.AboutUs.as_view(), name='about'),
    path('password_reset/', views.PasswordResetEnterEmail.as_view(), name='password_reset_enter_email'),
    path('password_reset/<str:encoded_email>/', views.CreateNewPassword.as_view(), name='create_password'),
]
