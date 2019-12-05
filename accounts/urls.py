from django.urls import path
from accounts import views as views

urlpatterns = [
    path('signup', views.SignUp.as_view(), name='signup'),
]
