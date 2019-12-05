from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as views

urlpatterns = [
    path('signup', views.SignUp.as_view(), name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='registeration/login.html'), name='login'),
]
